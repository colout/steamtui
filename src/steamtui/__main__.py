import Steam.TUI

def main ():
    ''' 
    Login process as grocked from Steam's unminified login.js (why don't they minify?!):
    
    1)  Get public key for my username from an endpoint.
    2)  Encrypt key and post to dologin enpdoint
    
    Notes:  
    - Does this mean they are saving passwords encrypted and reversable?!
    - I've never been captcha'd but I saw a recaptcha link.  Login might require javascript in the future, so this isn't futureproof
    - Found this https://gist.github.com/b1naryth1ef/8202642
    '''

    App = Steam.TUI.App()
    App.run()


if __name__ == "__main__":
    main()

