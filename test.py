import pandas as pd;
from Services.visualizeservice import fetchgolddata
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import faiss
import numpy as np
import os
# load_dotenv()

# os.environ['KAGGLEHUB_CACHE'] = os.path.abspath('./rawdata')
# os.environ['KAGGLE_API_TOKEN'] = os.getenv('KaggleAPIKey')

# import kagglehub
# cache_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
# print("Downloaded to:", cache_path)

# # Copy files to your clean target folder
# destination = "./data"
# os.makedirs(destination, exist_ok=True)

# for file in os.listdir(cache_path):
#     src = os.path.join(cache_path, file)
#     dst = os.path.join(destination, file)
#     if os.path.isfile(src):
#         shutil.copy(src, dst)

# print("Files copied to:", destination)
# print("Files:", os.listdir(destination))

def monthlyfeatures():

     sales, reviews = fetchgolddata()
     
     monthdf = sales.groupby("ORDERMONTH").agg(
          monthrev = ("TOTALREVENUE","sum"),
          monthorderitemcount = ("TOTALREVENUE" , "count"),
          monthordercount = ("ORDERID" , "nunique"),
          monthavgrevenue= ("TOTALREVENUE","mean")
     )
     monthdf.index = pd.to_datetime(monthdf.index, format="%Y-%m")
     full_range = pd.date_range(start=monthdf.index.min(), end=monthdf.index.max(), freq="MS")
     monthdf = monthdf.reindex(full_range, fill_value=0)
     monthdf.index = monthdf.index.strftime("%Y-%m")
     monthdf.index.name = "ORDERMONTH"

     monthdf["monthnumber"] = pd.to_datetime(monthdf.index, format="%Y-%m").month
     return monthdf


 


def trainmodel():
     df = monthlyfeatures()
     print("Total months:", len(df))
     print(df.index.tolist())
     encode = pd.get_dummies(df["monthnumber"], prefix="month")

     df = pd.concat([df,encode] , axis = 1)
     df= df.drop(columns =["monthnumber"])
     df["targetnextmonthrevenue"] = df["monthrev"].shift(-1)
     df = df.dropna(subset=["targetnextmonthrevenue"])
     X = df.drop(columns=["targetnextmonthrevenue"])
     y = df["targetnextmonthrevenue"]
     scaler = StandardScaler()
     numeric_cols = ["monthrev", "monthorderitemcount", "monthordercount", "monthavgrevenue"]
     X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
     model = LinearRegression()
     model.fit(X_train, y_train)       

     predictions = model.predict(X_test)
     comparison = pd.DataFrame({
         "actual": y_test.values,
         "predicted": predictions
     }, index=y_test.index)
     print(comparison)
     accuracy = r2_score(y_test, predictions)
     mae = mean_absolute_error(y_test, predictions)
     rmse = mean_squared_error(y_test, predictions) ** 0.5

     return {
    "r2_score": accuracy,
    "mae": mae,
    "rmse": rmse
}


# print(trainmodel())

from sentence_transformers import SentenceTransformer

def getreviewsforembedding():

    sales, reviews = fetchgolddata()
    df = reviews[["REVIEWID", "REVIEWCOMMENTMESSAGE"]]
    df = df.dropna(subset=["REVIEWCOMMENTMESSAGE"])
    df = df[df["REVIEWCOMMENTMESSAGE"].str.strip() != ""]
    return df

def generateembeddings(df):

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    review = df["REVIEWCOMMENTMESSAGE"].tolist()
    encode = model.encode(review)
    return df , encode
    
VECTOR_STORE_DIR = "./vectorstore"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def build_faiss_index(df, vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype('float32'))

    index_path = os.path.join(VECTOR_STORE_DIR, "review_index.faiss")
    mapping_path = os.path.join(VECTOR_STORE_DIR, "review_mapping.csv")

    faiss.write_index(index, index_path)
    df.reset_index(drop=True).to_csv(mapping_path, index=True)

    return index

# df = getreviewsforembedding()
# sample = df
# embedded_df, vectors = generateembeddings(sample)
# print(vectors.shape)
# print(vectors[0][:5])

# ind = build_faiss_index(embedded_df, vectors)
# print(ind)
def search_reviews(query, top_k=5):
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # Step 1: load the saved FAISS index and mapping
    index = faiss.read_index("./vectorstore/review_index.faiss")
    mapping = pd.read_csv("./vectorstore/review_mapping.csv")
    
    # Step 2: convert the query into a vector (same model, same process)
    query_vector = model.encode([query]).astype('float32')
    
    # Step 3: ask FAISS for the top_k closest matches
    distances, indices = index.search(query_vector, top_k)
    
    # Step 4: look up the actual review text using the returned positions
    results = mapping.iloc[indices[0]]
    
    return results

results = search_reviews("fast delivery, great product")
print(results)