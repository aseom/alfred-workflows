"""
Original script is part of 'pywebview' library
(C) 2014-2015 Roman Sirokov
Licensed under BSD license

http://github.com/r0x0r/pywebview/
"""

import Foundation
import AppKit
import WebKit
import PyObjCTools.AppHelper
from objc import nil

bundle = AppKit.NSBundle.mainBundle()
info = bundle.localizedInfoDictionary() or bundle.infoDictionary()

# This lines allow to load non-HTTPS resources, like a local app as: http://127.0.0.1:5000
info['NSAppTransportSecurity'] = {'NSAllowsArbitraryLoads': Foundation.YES}

# The app should not appear in the Dock or Force Quit window
info['LSUIElement'] = Foundation.YES


class BrowserView:
    instance = None
    app = AppKit.NSApplication.sharedApplication()

    class AppDelegate(AppKit.NSObject):
        def windowWillClose_(self, notification):
            BrowserView.app.stop_(self)

    class BrowserDelegate(AppKit.NSObject):
        def webView_contextMenuItemsForElement_defaultMenuItems_(self, webview, element, defaultMenuItems):
            return defaultMenuItems

    class WebKitHost(WebKit.WebView):
        def performKeyEquivalent_(self, theEvent):
            """
            Handle common hotkey shortcuts as copy/cut/paste/undo/select all/quit
            :param theEvent:
            :return:
            """

            if theEvent.type() == AppKit.NSKeyDown and theEvent.modifierFlags() & AppKit.NSCommandKeyMask:
                responder = self.window().firstResponder()
                keyCode = theEvent.keyCode()

                if responder != None:
                    handled = False
                    range_ = responder.selectedRange()
                    hasSelectedText = len(range_) > 0

                    if keyCode == 7 and hasSelectedText: #cut
                        responder.cut_(self)
                        handled = True
                    elif keyCode == 8 and hasSelectedText: #copy
                        responder.copy_(self)
                        handled = True
                    elif keyCode == 9: # paste
                        responder.paste_(self)
                        handled = True
                    elif keyCode == 0: # select all
                        responder.selectAll_(self)
                        handled = True
                    elif keyCode == 6: # undo
                        if responder.undoManager().canUndo():
                            responder.undoManager().undo()
                            handled = True
                    elif keyCode == 12 or keyCode == 13: # quit, close
                        BrowserView.app.terminate_(self)

                    return handled

    def __init__(self, title, url, width, height):
        BrowserView.instance = self

        screen = AppKit.NSScreen.mainScreen()
        x_pos = AppKit.NSWidth(screen.frame()) / 2 - width / 2
        y_pos = AppKit.NSHeight(screen.frame()) / 2 - height / 2

        rect = AppKit.NSMakeRect(x_pos, y_pos, width, height)
        window_mask = AppKit.NSTitledWindowMask | AppKit.NSClosableWindowMask | AppKit.NSMiniaturizableWindowMask
        window_mask = window_mask | AppKit.NSResizableWindowMask

        self.window = AppKit.NSWindow.alloc().\
            initWithContentRect_styleMask_backing_defer_(rect, window_mask, AppKit.NSBackingStoreBuffered, False)
        self.window.setTitle_(title)
        self.window.setMinSize_(AppKit.NSSize(200, 100))
        self.window.setLevel_(AppKit.NSFloatingWindowLevel)

        self.webkit = BrowserView.WebKitHost.alloc().initWithFrame_(rect)
        self.window.setContentView_(self.webkit)

        self._browserDelegate = BrowserView.BrowserDelegate.alloc().init()
        self._appDelegate = BrowserView.AppDelegate.alloc().init()
        self.webkit.setUIDelegate_(self._browserDelegate)
        self.window.setDelegate_(self._appDelegate)

        self.load_url(url)

    def show(self):
        self.window.display()
        self.window.orderFrontRegardless()
        BrowserView.app.run()

    def destroy(self):
        BrowserView.app.stop_(self)

    def load_url(self, url):
        def load(url):
            page_url = Foundation.NSURL.URLWithString_(url)
            req = Foundation.NSURLRequest.requestWithURL_(page_url)
            self.webkit.mainFrame().loadRequest_(req)

        self.url = url
        PyObjCTools.AppHelper.callAfter(load, url)
