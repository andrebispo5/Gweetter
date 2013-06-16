# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
import screenlets
import pango
import cairo
import gobject

class GWEETERScreenlet(screenlets.Screenlet):
    __name__ = 'GWEETER'
    __version__ = '0.1'
    __author__ = 'Andre Bispo'
    __desc__ = 'Simple Twitter Client Screenlet'
    text =  "######[GWEETTER CLIENT]######\n"
    __mousesel = 0
    interval = 180
    REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
    AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
    ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

    CONSUMER_KEY = "INSER_YOUR_KEY"
    CONSUMER_SECRET = "INSER_YOUR_SECRET"

    OAUTH_TOKEN = "INSER_YOUR_TOKEN"
    OAUTH_TOKEN_SECRET = "INSERT_YOU_TOKEN_SECRET"

    def __init__(self, **kwargs):
        # Customize the width and height.
        screenlets.Screenlet.__init__(self, width=300, height=700, **kwargs)
       

    def on_init(self):
        self.update()

    def on_draw(self, ctx):
        """Called every time the screenlet is drawn to the screen."""
        # Draw the background (a gradient).
        gradient = cairo.LinearGradient(0, self.height/2, 0, 0)
        gradient.add_color_stop_rgba(1, 0, 0.4, 1, 0.5)
        gradient.add_color_stop_rgba(1, 0, 0, 0, 0.4)
        ctx.set_source(gradient)
        self.draw_rectangle_advanced (ctx, 0, 0, self.width-20,
                                      self.height-20,
                                      rounded_angles=(5, 5, 5, 5),
                                      fill=True, border_size=3,
                                      border_color=(0, 0, 0, 0.25),
                                      shadow_size=10,
                                      shadow_color=(0, 0, 0, 0.25))
        
        # Make sure we have a pango layout initialized and updated.
        if self.p_layout == None :
            self.p_layout = ctx.create_layout()
        else:
            ctx.update_layout(self.p_layout)
            
        # Configure fonts.
        p_fdesc = pango.FontDescription()
        p_fdesc.set_family("Free Sans")
        p_fdesc.set_size(10 * pango.SCALE)
        self.p_layout.set_font_description(p_fdesc)

        # Display our text.
        pos = [0, 0]        
        ctx.set_source_rgb(1, 1, 1)
        text = self.text
        x = 0
        ctx.save()
        ctx.translate(*pos)
        self.draw_text(ctx, text, 20, 20, "Sans 9" , 10, self.width-35)
        pos[1] += 20
        ctx.restore()
        x += 1

    def on_draw_shape(self, ctx):
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()
        
    def on_mouse_move(self, event):
        """Called whenever the mouse moves over the screenlet."""
        x = event.x / self.scale
        y = event.y / self.scale
        self.__mousesel = int((y -10 )/ (20)) -1
        self.redraw_canvas()

    def get_oauth(self):
        oauth = OAuth1(self.CONSUMER_KEY,
                    client_secret=self.CONSUMER_SECRET,
                    resource_owner_key=self.OAUTH_TOKEN,
                    resource_owner_secret=self.OAUTH_TOKEN_SECRET)
        return oauth

    def update(self):
        self.text =  "######[GWEETTER CLIENT]######\n"
        oauth = self.get_oauth()
        count = 20
        r = requests.get(url="https://api.twitter.com/1.1/statuses/home_timeline.json?count={count}", auth=oauth)
        datajson = json.loads(r.text)
        dumpedtext = json.dumps(json.loads(r.text), indent=4, separators=(':',','))
        print dumpedtext
        for x in xrange(0,9):
            name = "[" + datajson[x]['user']['name'].encode('utf-8') + "]\n"
            twitt = datajson[x]['text'].encode('utf-8')
            self.text += "\n"
            self.text += name
            self.text += twitt
            self.text += "\n"
        self.redraw_canvas()
        # Set to update again after self.interval.
        self.__timeout = gobject.timeout_add(self.interval * 1000, self.update)

if __name__ == "__main__":
        import screenlets.session
    	screenlets.session.create_session(GWEETERScreenlet)


