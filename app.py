import flask
import pickle 
import pandas as pd
import numpy as np

# with open(f'model/book_rec_model.pkl','rb') as f:
#     model = pickle.load(f)

with open(f'model/book_ratings.pkl','rb') as f:
    ratings_df = pickle.load(f)

with open(f'model/book_details.pkl','rb') as f:
    df_books = pickle.load(f)

with open(f'model/training_data.pkl','rb') as f:
    train = pickle.load(f)

def create_book_ratings(book_df, book_index, ratings, n=10):
  book_ids = ratings_df.columns[book_index]
  book_ratings = pd.DataFrame(data=dict(bookId=book_ids, rating=ratings))
  top_n_books = book_ratings.sort_values("rating", ascending=False).head(n)
  
  book_recommendations = book_df[book_df.isbn.isin(top_n_books.bookId)].reset_index(drop=True)
  book_recommendations['rating'] = pd.Series(top_n_books.rating.values)
  return book_recommendations.sort_values("rating", ascending=False)

app = flask.Flask(__name__, template_folder='templates')
@app.route('/',methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':

        user_id = flask.request.form['ID']
        user_index = ratings_df.index.get_loc(user_id)
        # predictions_index = np.where(train[user_index, :] == 0)[0]

        existing_ratings_index = np.where(train[user_index, :] > 0)[0]
        existing_ratings = train[user_index, existing_ratings_index]

        exist = create_book_ratings(df_books, existing_ratings_index, existing_ratings)

        return(flask.render_template('main.html',original_input={'ID':user_id},result=exist))

if __name__ == '__main__':
    app.run()