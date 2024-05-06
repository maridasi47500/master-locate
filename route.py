from directory import Directory
from render_figure import RenderFigure
from myscript import Myscript
from user import User
from myrecording import Myrecording
from gagnant import Gagnant
from lyric import Lyric
from event import Event
from artist import Artist
from jeu import Jeu
from facturetel import Facturetel
from masterlocate import MasterLocate
from numero import Numero
try:
  from facebook import Facebook
except:
  print("attention faite export facebooktoken=\"\" avant de lancer le serveur")
from donneesfb import Donneesfb
from whatsapp import Whatsapp
from post import Post
from song import Song
from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.dbUsers=User()
        self.Program=Directory("premiere radio")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.dbScript=Myscript()
        self.dbRecording=Myrecording()
        self.dbPost=Post()
        self.dbFacturetel=Facturetel()
        self.dbWhatsapp=Whatsapp()
        self.dbDonneesfb=Donneesfb()
        self.facebook=Facebook()
        self.dbEvent=Event()
        self.dbNumero=Numero()
        self.masterLocate=MasterLocate
        self.dbJeu=Jeu()
        self.dbArtist=Artist()
        self.dbLyric=Lyric()
        self.dbGagnant=Gagnant()
        self.render_figure=RenderFigure(self.Program)
        self.getparams=("id",)
    def set_post_data(self,x):
        self.post_data=x
    def get_post_data(self):
        return self.post_data
    def set_my_session(self,x):
        print("set session",x)
        self.Program.set_my_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def set_redirect(self,x):
        self.Program.set_redirect(x)
        self.render_figure.set_redirect(self.Program.get_redirect())
    def render_some_html(self,x):
        return self.render_figure.render_some_html(x)
    def render_some_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_some_json(x)
    def render_my_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_my_json(x)
    def set_json(self,x):
        self.Program.set_json(x)
        self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
        print("set session",x)
        self.Program.set_session_params({"notice":x})
        self.render_figure.set_session(self.Program.get_session())
    def get_session_param(self,x):
          print("set session",x)
          self.Program.get_session()[x]
    def set_session(self,x):
          print("set session",x)
          self.Program.set_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def get_this_get_param(self,x,params):
          print("set session",x)
          hey={}
          for a in x:
              hey[a]=params[a][0]
          return hey
          
    def get_this_route_param(self,x,params):
          print("set session",x)
          return dict(zip(x,params["routeparams"]))
          
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def chat(self,search):
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/chat.html")
    def welcome(self,search):
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/index.html")
    def verifier(self,search):
        myparam=self.get_post_data()(params=("indicatif","num",))
        print(myparam)
        hi=self.masterLocate(myparam["indicatif"]+myparam["num"])
        print(hi)
        hey=hi.verifier()
        numero=hi.whatsapp_number()
        num=self.dbNumero.create({"numero": numero})
        self.set_session({"numero": numero})
        return self.render_some_html("welcome/hey.html")

    def audio_save(self,search):
        myparam=self.get_post_data()(params=("recording",))
        hi=self.dbRecording.create(myparam)
        return self.render_some_json("welcome/hey.json")
    def allscript(self,search):
        #myparam=self.get_post_data()(params=("name","content",))
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/allscript.html")
    def lancerscript(self,search):
        myparam=search["myid"][0]
        hi=self.dbScript.getbyid(myparam)
        print(hi, "my script")
        a=self.scriptpython(hi["name"]).lancer()
        return self.render_some_json("welcome/monscript.json")

    def monscript(self,search):
        myparam=self.get_post_data()(params=("name","content",))
        hey=self.dbCommandline.create(myparam)
        hi=self.dbScript.create(myparam)
        print(hey,hi)
        return self.render_some_json("welcome/monscript.json")
    def enregistrer(self,search):
        print("hello action")
        self.render_figure.set_param("enregistrer",True)
        return self.render_figure.render_figure("welcome/radio.html")
    def hello(self,search):
        print("hello action")
        return self.render_figure.render_figure("welcome/index.html")
    def passage(self,myscrit):
        filename=myscrit["title"][0].replace(".mp3","").split("/")[-1]
        current_dateTime=datetime.now()
        song=Song().save_heure_passage((filename,current_dateTime))
        self.render_figure.set_param("title", song["title"])
        self.render_figure.set_param("artist", song["artist"])
        self.render_figure.set_param("filename", song["filename"])
        self.render_figure.set_param("time", str(song["time"]))
        return self.render_some_json(Fichier("./welcome","chansonpassages.json").lire())
    def jouerchanson(self,myscrit):
        mylist=os.listdir("../radiohaker/public/uploads")
        k=random.randrange(0,(len(mylist) - 1))
        filename=mylist[k]
        print("filename =",filename)
        self.render_figure.set_param("filename", "/uploads/"+filename)
        song=Song().get_song((filename.replace(".mp3",""),))
        self.render_figure.set_param("title", song["title"])
        self.figure.set_param("artist", song["artist"])
        self.render_some_json(Fichier("./welcome","chansons.json").lire())
    def delete_user(self,params={}):
        getparams=("id",)
        myparam=self.post_data(self.getparams)
        self.render_figure.set_param("user",User().deletebyid(myparam["id"]))
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def edit_user(self,params={}):
        getparams=("id",)

        myparam=self.get_this_route_param(getparams,params)
        print("route params")
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("user/edituser.html")
    def seeuser(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        return self.render_figure.set_param("user",User().getbyid(myparam["id"]))
    def myusers(self,params={}):
        self.render_figure.set_param("users",User().getall())
        return self.render_figure.render_figure("user/users.html")
    def donneeswhatsap(self,params={}):
        myparam=self.post_data(("file",))
        myfile=myparam["file"]
        num=self.dbNumero.getbynumero(self.get_session_param("numero"))["id"]
        self.dbWhatsapp.create({"numero_id":num,"file":myfile})

        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def facturetelephone(self,params={}):
        myparam=self.post_data(("file",))
        myfile=myparam["file"]
        num=self.dbNumero.getbynumero(self.get_session_param("numero"))["id"]
        self.dbFacturetel.create({"numero_id":num,"file":myfile})
        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def lienpost(self,params={}):
        myparam=self.post_data(("lien",))
        myid=myparam["lien"]
        self.facebook.get_post(myid)
        text=self.facebook.get_post_text()
        self.dbPost.create({"postid":myid,"text":text})
        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def event(self,params={}):
        myparam=self.post_data(("lien",))
        myid=myparam["lien"]
        self.facebook.get_event(myid)
        name=self.facebook.get_event_name()
        self.dbEvent.create({"eventid":myid,"name":name})
        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def donneesfb(self,params={}):
        myparam=self.post_data(("file",))
        myfile=myparam["file"]
        num=self.dbNumero.getbynumero(self.get_session_param("numero"))["id"]
        self.dbDonneesfb.create({"numero_id":num,"file":myfile})
        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def newpostfb(self,params={}):
        myparam=self.post_data(("text",))
        text=myparam["text"]
        self.facebook.create_post(text)
        post_id=self.facebook.get_post_id()
        self.dbPost.create({"postid":post_id,"text":text})
        self.set_json("{\"redirect\":\"/new\"}")
        return self.render_figure.render_json()
    def update_user(self,params={}):
        myparam=self.post_data(self.getparams)
        self.user=self.dbUsers.update(params)
        self.set_session(self.user)
        self.set_redirect(("/seeuser/"+params["id"][0]))
    def login(self,s):
        search=self.get_post_data()(params=("email","password"))
        self.user=self.dbUsers.getbyemailpw(search["email"],search["password"])
        print("user trouve", self.user)
        if self.user["email"]:
            self.set_session(self.user)
            self.set_json("{\"redirect\":\"/\"}")

        else:
            self.set_json("{\"redirect\":\"/signin\"}")
            print("session login",self.Program.get_session())
        return self.render_figure.render_json()
    def nouveau(self,search):
        return self.render_figure.render_figure("welcome/new.html")
    def chanson(self,params={}):
        myparam=self.get_post_data()(params=("title","artist","file","lyric"))


        return self.render_some_json("welcome/create.json")
    def getlyrics(self,params={}):
        getparams=("id",)

       
        myparam=self.get_this_get_param(getparams,params)
        print("my param :",myparam)
        try:
          hey=self.dbLyric.getbysongid(myparam["id"])
          print("hey",hey)
          if not hey:
            hey=[]
        except:
          hey=[]

        self.render_figure.set_param("lyrics",hey)
        return self.render_some_json("welcome/lyrics.json")
    def photoartist(self,params={}):
        myparam=self.get_post_data()(params=("pic","id",))
        hey=self.dbArtist.update(myparam)
        return self.render_some_json("welcome/create.json")
        return self.render_some_json("welcome/create.json")
    def jouerjeux(self,search):
        return self.render_figure.render_figure("welcome/jeu.html")
    def monjeu(self,search):
        myparam=self.get_post_data()(params=("lyric_id",))

        hi=self.dbJeu.createwithlyric(myparam)
        print(hi)
        self.render_figure.set_param("redirect","/jouerjeux")
        return self.render_some_json("welcome/redirect.json")
    def gagnant(self,search):
        myparam=self.get_post_data()(params=("name","pic",))

        hi=self.dbGagnant.create(myparam)
        print(hi)
        return self.render_some_json("welcome/create.json")

    def signin(self,search):
        return self.render_figure.render_figure("user/signin.html")

    def save_user(self,params={}):
        myparam=self.get_post_data()(params=("email", "nomcomplet","password","password_confirmation"))
        self.user=self.dbUsers.create(myparam)
        if self.user["email"]:
            self.set_json("{\"redirect\":\"/\"}")
            self.set_session(self.user)
        else:
            self.set_json("{\"redirect\":\"/signin\"}")
        return self.render_figure.render_json()
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if post_data:
            print("post data")
            self.set_post_data(post_data)
            print("post data set",post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("png"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("gif"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("svg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            path=path.split("?")[0]
            print("link route ",path)
            ROUTES={
                    '^/new$': self.nouveau,
                    '^/verifier$': self.verifier,
                    '^/welcome$': self.welcome,
                    '^/event$': self.event,
                    '^/newpostfb$': self.newpostfb,
                    '^/lienpost$': self.lienpost,
                    '^/donneeswhatsap$': self.donneeswhatsap,
                    '^/facturetelephone$': self.facturetelephone,
                    '^/donneesfb$': self.donneesfb,
                    '^/signin$': self.signin,
                    '^/audio_save$': self.audio_save,
                    '^/recordsomething$': self.enregistrer,
                    r"^/songs/jouerunechanson$":self.jouerchanson,
                    r"^/songs/playmusique1$":self.jouerchanson,
                    r"^/songs/playmusique$":self.jouerchanson,
                    '^/logmeout$':self.logout,
                                        '^/save_user$':self.save_user,
                                                            '^/update_user$':self.update_user,
                    r"^/songs/musique$":self.jouerchanson,
                    r"^/passage$":self.passage,
                    '^/monscript$': self.monscript,
                    "^/seeuser/([0-9]+)$":self.seeuser,
                                        "^/edituser/([0-9]+)$":self.edit_user,
                                                            "^/deleteuser/([0-9]+)$":self.delete_user,
                                                                                '^/login$':self.login,

                                                                                                    '^/users$':self.myusers,
                    '^/$': self.hello

                    }
            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               if x:
                   params["routeparams"]=x.groups()
                   try:
                       self.Program.set_html(html=mycase(params))


                   except Exception:  
                       self.Program.set_html(html="<p>une erreur s'est produite "+str(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>")
                   #self.Program.redirect_if_not_logged_in()

                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
        return self.Program
