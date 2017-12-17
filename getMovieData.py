# -*- coding: UTF-8 -*-

import urllib
import json
import time
import web

db = web.database(dbn = 'sqlite', db = 'MovieSite.db')

class getMovieData:
	'''
		1. 从豆瓣Api获取影片信息
		2. 将电影图片获取到本地
		3. 将获取的影片信息存入数据库中
	'''

	def getAllMovieAndIds(self):
		movie_ids = []
		movies = []
		for index in range(0, 250, 50):
			response = urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50' % index)

			data = response.read()

			data_json = json.loads(data)

			movie250 = data_json['subjects']
			movies.append(movie250)

			for movie in movie250:
				movie_ids.append(movie['id'])

			time.sleep(3)
		return movie_ids

	def getMovieDetail(self):
		
		ids = self.getAllMovieAndIds()

		count = 0
		for mid in ids:
			response = urllib.urlopen('http://api.douban.com/v2/movie/subject/%s' % mid)

			data = response.read()
			movie = json.loads(data)

			if movie.has_key('id'):
				self.add_movie(movie)

				self.get_poster(movie)
				count += 1
				time.sleep(3)
			else:
				print movie

	def add_movie(self, movie):
		db.insert(
			'movie',
			id=int(movie['id']),
			title=movie['title'] or 'undefind',
			origin = movie['original_title'],
			url = movie['alt'],
			rating = movie['rating']['average'],
			image = movie['images']['large'],
			directors = ','.join([d['name'] for d in movie['directors']]),
			casts = ','.join([c['name'] for c in movie['casts']]),
			year = movie['year'],
			genres = ','.join(movie['genres']),
			countries = ','.join(movie['countries']),
			summary = movie['summary']
		)

	def get_poster(self, movie):
		pic = urllib.urlopen(movie['images']['large']).read();
		fileName = 'static/poster/%d.jpg' % int(movie['id'])
		f = file(fileName, 'wb')
		f.write(pic)
		f.close()


if __name__ == '__main__':
	getMovie = getMovieData()
	getMovie.getAllMovieAndIds()
	getMovie.getMovieDetail()