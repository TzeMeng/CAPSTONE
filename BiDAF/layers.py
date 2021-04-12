import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from utils import masked_softmax
import config

# class Embedding(nn.Module):
#     """Embedding layer used by BiDAF, with Words and Characters.
#     Args:
#         word_vectors (torch.Tensor): Pre-trained word vectors.
#         char_vectors (torch.Tensor): Randomly initialized char vectors
#         hidden_size (int): Size of hidden activations.
#         drop_prob (float): Probability of zero-ing out activations
#     """
#     def __init__(self, word_vectors, char_vectors, hidden_size, drop_prob):
#         super(Embedding, self).__init__()
#         self.drop_prob = drop_prob
#         self.w_embed = nn.Embedding.from_pretrained(word_vectors, freeze=True)
#         self.c_embed = nn.Embedding.from_pretrained(char_vectors, freeze=False)
#         self.proj = nn.Linear(word_vectors.size(1), hidden_size, bias=False)
#         self.char_conv = nn.Conv2d(1, config.char_channel_size, (config.char_embedding_size, config.char_channel_width))
#         self.hwy = HighwayEncoder(2, hidden_size * 2)

#     def forward(self, x, y):
#         batch_size = x.size(0)

#         w_emb = self.w_embed(x)   # (batch_size, seq_len, embed_size)
#         w_emb = F.dropout(w_emb, self.drop_prob, self.training)
#         w_emb = self.proj(w_emb)  # (batch_size, seq_len, hidden_size)

#         c_emb = self.c_embed(y)
#         c_emb = F.dropout(c_emb, self.drop_prob, self.training)
#         c_emb = c_emb.view(-1, config.char_embedding_size, c_emb.size(2)).unsqueeze(1)
#         c_emb = self.char_conv(c_emb).squeeze()
#         c_emb = F.max_pool1d(c_emb, c_emb.size(2)).squeeze()
#         c_emb = c_emb.view(batch_size, -1, config.char_channel_size)

#         emb = torch.cat([w_emb, c_emb], dim=-1)

#         emb = self.hwy(emb)   # (batch_size, seq_len, hidden_size)
#         return emb


class Embedding(nn.Module):
    """Embedding layer used by BiDAF, with Words and Characters.
    Args:
        word_vectors (torch.Tensor): Pre-trained word vectors.
        char_vectors (torch.Tensor): Randomly initialized char vectors
        hidden_size (int): Size of hidden activations.
        drop_prob (float): Probability of zero-ing out activations
    """
    def __init__(self, word_vectors, char_vectors, hidden_size, drop_prob):
        super(Embedding, self).__init__()
        self.drop_prob = drop_prob
        self.w_embed = nn.Embedding.from_pretrained(word_vectors, freeze=True)
        self.c_embed = nn.Embedding.from_pretrained(char_vectors, freeze=False)
        self.proj = nn.Linear(word_vectors.size(1), hidden_size, bias=False)
        # self.char_conv = nn.Conv2d(1, config.char_channel_size, (config.char_embedding_size, config.char_channel_width))
        self.char_conv = CNN(in_channels=char_vectors.size(1), out_channels=hidden_size)
        self.hwy = HighwayEncoder(2, hidden_size * 2)


    def forward(self, x, y):
        batch_size = x.size(0)

        w_emb = self.w_embed(x)   # (batch_size, seq_len, embed_size)
        w_emb = F.dropout(w_emb, self.drop_prob, self.training)
        w_emb = self.proj(w_emb)  # (batch_size, seq_len, hidden_size)

        batch_size, sentence_length, max_word_length = y.size()

        y = y.contiguous().view(-1, max_word_length)
        y = self.c_embed(y)
        y = F.dropout(y, self.drop_prob, self.training)

        c_emb1 = self.char_conv(y.permute(0, 2, 1), sentence_length, batch_size)
        # c_emb = self.c_embed(y)
        # c_emb = F.dropout(c_emb, self.drop_prob, self.training)
        # c_emb = c_emb.view(-1, config.char_embedding_size, c_emb.size(2)).unsqueeze(1)
        # c_emb = self.char_conv(c_emb).squeeze()
        # c_emb = F.max_pool1d(c_emb, c_emb.size(2)).squeeze()
        # c_emb = c_emb.view(batch_size, -1, config.char_channel_size)

        # emb = torch.cat([w_emb, c_emb], dim=-1)

        # emb = self.hwy(emb)   # (batch_size, seq_len, hidden_size)

        # return emb
        concat_emb = torch.cat((c_emb1, w_emb), 2)

        hwy_out = self.hwy(concat_emb)

        return hwy_out

class CNN(nn.Module):
    """A CNN layer for character embeddings, for detailes see https://arxiv.org/abs/1611.01603.
    Args:
        char_vectors (torch.Tensor): Pre-trained char vectors.
        hidden_size (int): Size of hidden activations.
        drop_prob (float): Probability of zero-ing out activations
    """
    def __init__(self, in_channels, out_channels):
        super(CNN, self).__init__()
        self.out_channels = out_channels
        self.conv1d_1 = nn.Conv1d(in_channels, out_channels, kernel_size=5, bias=True)
        self.conv1d_2 = nn.Conv1d(out_channels, out_channels, kernel_size=3, bias=True)
        self.conv1_bn = nn.BatchNorm1d(out_channels)
        self.conv2_bn = nn.BatchNorm1d(out_channels)

    def forward(self, x, sentence_length, batch_size):
        conv_1 = self.conv1d_1(x)
        conv_1 = F.relu(conv_1)
        #conv_1 = self.conv1_bn(conv_1)
        conv_1 = F.dropout(conv_1, config.drop_prob, self.training)
        conv_1 = self.conv1_bn(conv_1)

        conv_out_1 = torch.max(conv_1, dim=-1)[0]
        conv_out_1 = conv_out_1.view(batch_size, sentence_length, self.out_channels)

        conv_2 = self.conv1d_2(conv_1)
        conv_2 = F.relu(conv_2)
        conv_2 = self.conv2_bn(conv_2)
        conv_out_2 = torch.max(conv_2, dim=-1)[0]
        conv_out_2 = conv_out_2.view(batch_size, sentence_length, self.out_channels)

        # print(conv_out_2.shape)

        # concat_conv = torch.cat((conv_out_1, conv_out_2), 2)
        
        return conv_out_2

class HighwayEncoder(nn.Module):
    """Encode an input sequence using a highway network.
    Based on the paper:
    "Highway Networks"
    by Rupesh Kumar Srivastava, Klaus Greff, Jürgen Schmidhuber
    (https://arxiv.org/abs/1505.00387).
    Args:
        num_layers (int): Number of layers in the highway encoder.
        hidden_size (int): Size of hidden activations.
    """
    def __init__(self, num_layers, hidden_size):
        super(HighwayEncoder, self).__init__()
        self.transforms = nn.ModuleList([nn.Linear(hidden_size, hidden_size)
                                         for _ in range(num_layers)])
        self.gates = nn.ModuleList([nn.Linear(hidden_size, hidden_size)
                                    for _ in range(num_layers)])

    def forward(self, x):
        for gate, transform in zip(self.gates, self.transforms):
            # Shapes of g, t, and x are all (batch_size, seq_len, hidden_size)
            g = torch.sigmoid(gate(x))
            t = F.relu(transform(x))
            x = g * t + (1 - g) * x

        return x


class RNNEncoder(nn.Module):
    """General-purpose layer for encoding a sequence using a bidirectional RNN.
    Encoded output is the RNN's hidden state at each position, which
    has shape `(batch_size, seq_len, hidden_size * 2)`.
    Args:
        input_size (int): Size of a single timestep in the input.
        hidden_size (int): Size of the RNN hidden state.
        num_layers (int): Number of layers of RNN cells to use.
        drop_prob (float): Probability of zero-ing out activations.
    """
    def __init__(self,
                 input_size,
                 hidden_size,
                 num_layers,
                 drop_prob=0.):
        super(RNNEncoder, self).__init__()
        self.drop_prob = drop_prob
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers,
                           batch_first=True,
                           bidirectional=True,
                           dropout=drop_prob if num_layers > 1 else 0.)

    def forward(self, x, lengths):
        # Save original padded length for use by pad_packed_sequence
        orig_len = x.size(1)

        # Sort by length and pack sequence for RNN
        lengths, sort_idx = lengths.sort(0, descending=True)
        x = x[sort_idx]     # (batch_size, seq_len, input_size)
        x = pack_padded_sequence(x, lengths, batch_first=True)

        # Apply RNN
        x, _ = self.rnn(x)  # (batch_size, seq_len, 2 * hidden_size)

        # Unpack and reverse sort
        x, _ = pad_packed_sequence(x, batch_first=True, total_length=orig_len)
        _, unsort_idx = sort_idx.sort(0)
        x = x[unsort_idx]   # (batch_size, seq_len, 2 * hidden_size)

        # Apply dropout (RNN applies dropout after all but the last layer)
        x = F.dropout(x, self.drop_prob, self.training)

        return x


class BiDAFAttention(nn.Module):
    """Bidirectional attention originally used by BiDAF.
    Bidirectional attention computes attention in two directions:
    The context attends to the query and the query attends to the context.
    The output of this layer is the concatenation of [context, c2q_attention,
    context * c2q_attention, context * q2c_attention]. This concatenation allows
    the attention vector at each timestep, along with the embeddings from
    previous layers, to flow through the attention layer to the modeling layer.
    The output has shape (batch_size, context_len, 8 * hidden_size).
    Args:
        hidden_size (int): Size of hidden activations.
        drop_prob (float): Probability of zero-ing out activations.
    """
    def __init__(self, hidden_size, drop_prob=0.1):
        super(BiDAFAttention, self).__init__()
        self.drop_prob = drop_prob
        self.c_weight = nn.Parameter(torch.zeros(hidden_size, 1))
        self.q_weight = nn.Parameter(torch.zeros(hidden_size, 1))
        self.cq_weight = nn.Parameter(torch.zeros(1, 1, hidden_size))
        for weight in (self.c_weight, self.q_weight, self.cq_weight):
            nn.init.xavier_uniform_(weight)
        self.bias = nn.Parameter(torch.zeros(1))

    def forward(self, c, q, c_mask, q_mask):
        batch_size, c_len, _ = c.size()
        q_len = q.size(1)
        s = self.get_similarity_matrix(c, q)        # (batch_size, c_len, q_len)
        c_mask = c_mask.view(batch_size, c_len, 1)  # (batch_size, c_len, 1)
        q_mask = q_mask.view(batch_size, 1, q_len)  # (batch_size, 1, q_len)
        s1 = masked_softmax(s, q_mask, dim=2)       # (batch_size, c_len, q_len)
        s2 = masked_softmax(s, c_mask, dim=1)       # (batch_size, c_len, q_len)

        # (bs, c_len, q_len) x (bs, q_len, hid_size) => (bs, c_len, hid_size)
        a = torch.bmm(s1, q)
        # (bs, c_len, c_len) x (bs, c_len, hid_size) => (bs, c_len, hid_size)
        b = torch.bmm(torch.bmm(s1, s2.transpose(1, 2)), c)

        x = torch.cat([c, a, c * a, c * b], dim=2)  # (bs, c_len, 4 * hid_size)

        return x

    def get_similarity_matrix(self, c, q):
        """Get the "similarity matrix" between context and query (using the
        terminology of the BiDAF paper).
        A naive implementation as described in BiDAF would concatenate the
        three vectors then project the result with a single weight matrix. This
        method is a more memory-efficient implementation of the same operation.
        See Also:
            Equation 1 in https://arxiv.org/abs/1611.01603
        """
        c_len, q_len = c.size(1), q.size(1)
        c = F.dropout(c, self.drop_prob, self.training)  # (bs, c_len, hid_size)
        q = F.dropout(q, self.drop_prob, self.training)  # (bs, q_len, hid_size)

        # Shapes: (batch_size, c_len, q_len)
        s0 = torch.matmul(c, self.c_weight).expand([-1, -1, q_len])
        s1 = torch.matmul(q, self.q_weight).transpose(1, 2)\
                                           .expand([-1, c_len, -1])
        s2 = torch.matmul(c * self.cq_weight, q.transpose(1, 2))
        s = s0 + s1 + s2 + self.bias

        return s


class BiDAFOutput(nn.Module):
    """Output layer used by BiDAF for question answering.
    Computes a linear transformation of the attention and modeling
    outputs, then takes the softmax of the result to get the start pointer.
    A bidirectional LSTM is then applied the modeling output to produce `mod_2`.
    A second linear+softmax of the attention output and `mod_2` is used
    to get the end pointer.
    Args:
        hidden_size (int): Hidden size used in the BiDAF model.
        drop_prob (float): Probability of zero-ing out activations.
    """
    def __init__(self, hidden_size, drop_prob):
        super(BiDAFOutput, self).__init__()
        self.att_linear_1 = nn.Linear(8 * hidden_size, 1)
        self.mod_linear_1 = nn.Linear(2 * hidden_size, 1)

        self.rnn = RNNEncoder(input_size=2 * hidden_size,
                              hidden_size=hidden_size,
                              num_layers=1,
                              drop_prob=drop_prob)

        self.att_linear_2 = nn.Linear(8 * hidden_size, 1)
        self.mod_linear_2 = nn.Linear(2 * hidden_size, 1)

    def forward(self, att, mod, mask):
        # Shapes: (batch_size, seq_len, 1)
        logits_1 = self.att_linear_1(att) + self.mod_linear_1(mod)
        mod_2 = self.rnn(mod, mask.sum(-1))
        logits_2 = self.att_linear_2(att) + self.mod_linear_2(mod_2)

        # Shapes: (batch_size, seq_len)
        log_p1 = masked_softmax(logits_1.squeeze(), mask, log_softmax=True)
        log_p2 = masked_softmax(logits_2.squeeze(), mask, log_softmax=True)

        return log_p1, log_p2