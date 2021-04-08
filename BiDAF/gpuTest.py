import tensorflow as tf

# with tf.compat.v1.Session() as sess:
#     with tf.device('/gpu:0'):
#         a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
#         b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
#         c = tf.matmul(a, b)
#     print (sess.run(c))

with tf.device('/gpu:0'):
    original = tf.constant([1,0.8,0.6,0.8,1,0.8,0.6,0.8,1], shape=[3, 3], name='original')
    a = tf.constant([0.32,-0.32,0.04,-0.32,0.64,-0.32,0.04,-0.32,0.32], shape=[3, 3], name='a')
    # b = tf.constant([0.8,0.6,0.2], shape=[3, 1], name='b')
    # c = (1/0.088) * a
    # d = tf.matmul(c , b)
    print (tf.linalg.inv(original))
    print (tf.linalg.det(original)^-1)