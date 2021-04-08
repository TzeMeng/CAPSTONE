const admin = require('./node_modules/firebase-admin');
const serviceAccount = require("./capstone-dsta-firebase-adminsdk-2kf8q-d29d9acd3a.json");
const data = require("./data2.json");
const collectionKey = "New_squad2"; //name of the collection
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://capstone-dsta-default-rtdb.firebaseio.com"
});
const firestore = admin.firestore();
const settings = {timestampsInSnapshots: true};
firestore.settings(settings);
if (data && (typeof data === "object")) {
Object.keys(data).forEach(docKey => {
 firestore.collection(collectionKey).doc(docKey).set(data[docKey]).then((res) => {
    console.log("Document " + docKey + " successfully written!");
}).catch((error) => {
   console.error("Error writing document: ", error);
});
});
}