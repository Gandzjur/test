import tornado.escape
import tornado.ioloop
import tornado.web


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/get_data", SignalProcessorHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, I am Tornado app!")


class SignalProcessorHandler(tornado.web.RequestHandler):
    @staticmethod
    def toValidOutput(params):
        for index, param in enumerate(params):
            if param == "1" or param == "True":
                params[index] = "1"
            elif param == "0" or param == "False":
                params[index] = "0"
            else:
                return "Invalid value of 'flag'", 1
        flags = "".join(params)
        symbol_codes = [int(flags[0:8][::-1], 2), int(flags[8:16][::-1], 2)]
        data = "".join(map(chr, symbol_codes))
        return data, 0

    def get(self):
        params = [self.get_query_argument("f{}".format(i), "0") for i in xrange(16)]
        data, err = self.toValidOutput(params)
        self.write(data)

    def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except ValueError, e:
            self.write(dict(data=e.message, error_code=2))
        else:
            params = [str(json_request.get("f{}".format(i), "0")) for i in xrange(16)]
            data, err_code = self.toValidOutput(params)
            self.write(dict(data=data.decode(), error_code=err_code))

if __name__ == '__main__':
    application = Application()
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
