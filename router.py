# -*- coding: UTF-8 -*-

from Logics import views 

urls = (
	r'/', views.index,
	r'/movie/(\d+)', views.movie,
)