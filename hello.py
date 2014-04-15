import urllib2
import pprint
import json

from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/github', methods=['GET','POST'])
def github():
	username = request.form['username']
	link =  "https://api.github.com/users/%s/repos?per_page=100" % (username)
	user_link = "https://api.github.com/users/%s" % (username)
	response = urllib2.urlopen(link)
	user_response = urllib2.urlopen(user_link)
	html = response.read()
	html1 = user_response.read()
	repos = json.loads(html)
	user_git = json.loads(html1)
	sorted_repo = sorted(repos, key=lambda repo: repo['forks_count'], reverse=True)
	pprint.pprint(sorted_repo[:5])

	return render_template('github.html',
		avatar=repos[0]['owner']['avatar_url'],
		name=repos[0]['owner']['login'],
		repo_names=[repo['name'] for repo in sorted_repo[:5]],
		user_area=user_git['location'],
		user_bio=user_git['bio'],
		git_name=user_git['name']

		)

if __name__ == '__main__':
	app.run()
	app.debug = True