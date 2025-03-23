from fastapi import APIRouter, Query
import requests
import json

router = APIRouter()

def fetch_firebase_docs(function_name):
    # Extract specific function if format like "firebase.auth.signIn"
    if function_name.startswith("firebase."):
        function_name = function_name[9:]  # Remove "firebase." prefix
    
    # Mock documentation for different Firebase functions
    mock_docs = {
        "auth.signIn": """
        # firebase.auth.signIn
        
        Signs in a user with the provided email and password.
        
        ## Parameters:
        - email (string): Required. The user's email address.
        - password (string): Required. The user's password.
        
        ## Returns:
        - UserCredential: Contains an access token and information about the user.
        
        ## Example:
        ```javascript
        import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
        
        const auth = getAuth();
        signInWithEmailAndPassword(auth, email, password)
          .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;
            // ...
          })
          .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
          });
        ```
        """,
        "firestore.collection": """
        # firebase.firestore.collection
        
        Gets a CollectionReference instance that refers to the collection at the specified path.
        
        ## Parameters:
        - path (string): Required. Path to the collection.
        
        ## Returns:
        - CollectionReference: A reference to the collection.
        
        ## Example:
        ```javascript
        import { collection, getDocs } from "firebase/firestore";
        
        const querySnapshot = await getDocs(collection(db, "cities"));
        querySnapshot.forEach((doc) => {
          console.log(`${doc.id} => ${doc.data()}`);
        });
        ```
        """
    }
    
    # If function is in our mock data, return it
    for key in mock_docs:
        if key.lower() in function_name.lower():
            return mock_docs[key]
    
    # Default fallback
    return f"Documentation for {function_name} not found. Please check the Firebase documentation at https://firebase.google.com/docs/reference"

@router.get("/firebase/context")
async def firebase_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_firebase_docs(function)
    
    return {
        "context": {
            "language": language,
            "library": "firebase",
            "function": function,
            "documentation": doc_snippet
        }
    } 