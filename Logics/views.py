# -*- coding: UTF-8 -*-

import web

render = web.template.render('templates/')

db = web.database(dbn='sqlite', db='MovieSite.db')

class index:
	def GET(self):
			movies = db.select('movie')
			print movies
			return render.index(movies)

	def POST(self):
		data = web.input()
		condition = r'title like "%' + data.title + r'%"'
		movies = db.select('movie', where=condition)
		return render.index(movies)


class movie:
	"""docstring for movie"""

	def GET(self, movieId):
		movie_id = int(movieId)
		movie = db.select('movie', where='id=$movie_id', vars=locals())[0]
		return render.movie(movie)

		
