
import web
import router


if __name__ == '__main__':

	app = web.application(router.urls, globals())
	app.run()