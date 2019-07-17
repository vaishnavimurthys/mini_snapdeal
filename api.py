from flask import Flask,render_template,request,redirect,url_for,session
from models.model1 import user_exists,save_user,add_product,product_exists


app = Flask(__name__)
app.secret_key='hello'

@app.route('/')
def home():

	return render_template('home.html',title='home')

@app.route('/about')
def about():

	return render_template('about.html',title='about')

@app.route('/contact')
def contact():

	return render_template('contact.html',title='contact')


@app.route('/login',methods=['GET','POST'])
def login():
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']

			result=user_exists(username)
			if result:


				if result['password']!=password:
					return "password doesnt match.Go back and enter valid username "

				session['username'] = username
				session['c_type']=result['c_type']
				return redirect(url_for('home'))
			return "username doesnt exists"
		return redirect(url_for('home'))


@app.route('/signup',methods=['GET','POST'])
def signup():

	if request.method=='POST':

		user_info={}

		user_info['username']=request.form['username']
		user_info['password']=request.form['password1']
		password2=request.form['password2']
		user_info['c_type']=request.form['type']
		if user_info['c_type']=='buyer':
			user_info['cart']= []
		if user_exists(user_info['username']):
			return"username already exists"
		if user_info['password']!=password2:
			return "passwords dont match"
		save_user(user_info)
		return redirect(url_for('home'))




	return redirect(url_for('home'))

@app.route('/products', methods=['GET','POST'])
def products():
	if request.method=='POST':
		product_info={}
		product_info['name']=request.form['name']
		product_info['price']=int(request.form['price'])
		product_info['description']=request.form['description']
		product_info['seller']=session['username']

		if product_exists(product_info['name']):
			return "product exists"
		add_product(product_info)
		return "product added ! check your db"
	return(redirect(url_for('home')))

@app.route('/logout')
def logout():
			session.clear()
			return redirect(url_for('home'))


app.run(debug=True)