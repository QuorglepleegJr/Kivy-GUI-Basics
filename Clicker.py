from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from threading import Timer # To create "clicks" every second

from sys import exit

class Clicker(App):

  __BASE_CLICKER_COST = 10
  __BASE_BOT_NET_COST = 100
  __GROWTH_RATE = 1.5


  def __init__(self, *args):
    super(Clicker, self).__init__(*args)
    self.__clicks = 0
    self.__clickers = 0
    self.__bot_nets = 0

    self.__clicker_cost = None
    self.__10_clicker_cost = None
    self.__bot_net_cost = None
    self.__10_bot_net_cost = None
    self.__calculateCosts()

    self.__clicker_sell = None
    self.__10_clicker_sell = None
    self.__bot_net_sell = None
    self.__10_bot_net_sell = None
    self.__calculateSells()
    
    self.__buttons_pipe = []

  def build(self):


    self.__main_button = Button(text="Clicks: 0")
    
    self.__clickers_label = Label(text="Clickers: 0")
    self.__bot_nets_label = Label(text="Bot Nets: 0")

    self.__buy_clicker_button = Button(text="Buy 1: 0")
    self.__buy_10_clicker_button = Button(text="Buy 10: 0")
    self.__sell_clicker_button = Button(text="Sell 1: 0")
    self.__sell_10_clicker_button = Button(text="Sell 10: 0")
    self.__buy_bot_net_button = Button(text="Buy 1: 0")
    self.__buy_10_bot_net_button = Button(text="Buy 10: 0")
    self.__sell_bot_net_button = Button(text="Sell 1: 0")
    self.__sell_10_bot_net_button = Button(text="Sell 10: 0")

    #for attribute in dir(self): # Lazy solution to writing out all buttons, should probably replace
      #if "button" in attribute:
        #self.__getattribute__(attribute).bind(self.__handleButtons)

    
    clicker_menu_elements = [
      self.__buy_10_clicker_button,
      self.__buy_clicker_button,
      self.__sell_clicker_button,
      self.__sell_10_clicker_button,
      ]
    
    clicker_menu = BoxLayout(orientation="horizontal")
    for element in clicker_menu_elements:
      clicker_menu.add_widget(element)

    bot_net_menu_elements = [
      self.__buy_10_bot_net_button,
      self.__buy_bot_net_button,
      self.__sell_bot_net_button,
      self.__sell_10_bot_net_button,
      ]
    
    bot_net_menu = BoxLayout(orientation="horizontal")
    for element in bot_net_menu_elements:
      bot_net_menu.add_widget(element)

    right_elements = [
      self.__clickers_label,
      clicker_menu,
      self.__bot_nets_label,
      bot_net_menu,
      ]

    right_menu = BoxLayout(orientation="vertical")
    for element in right_elements:
      right_menu.add_widget(element)

    main_elements = [
      self.__main_button,
      right_menu,
      ]

    main_layout = BoxLayout(orientation="horizontal")
    for element in main_elements:
      main_layout.add_widget(element)

    Clock.schedule_interval(self.mainLoop, 0.02)

    return main_layout

  def mainLoop(self, nap):
    print("Main Loop")
    while len(self.__buttons_pipe) > 0:
      button = self.__buttons_pipe.pop(0)
      print("Button:", button) # Not printing, fix
      # Make it handle each individual button

  def handleButtons(self, instance):
    self.__buttons_pipe.append(instance)

  def __handleMainButton(self):
    self.__click()

  def __handleBuyClicker(self):
    if self.__clicks >= self.__clicker_cost:
      self.__clicks -= self.__clicker_cost
      self.__clickers += 1

  def __handleBuy10Clickers(self):
    if self.__clicks >= self.__10_clicker_cost:
      self.__clicks -= self.__10_clicker_cost
      self.__clickers += 10

  def __handleBuyBotNet(self):
    if self.__clicks >= self.__bot_net_cost:
      self.__clicks -= self.__bot_net_cost
      self.__bot_nets += 1

  def __handleBuy10BotNets(self):
    if self.__clicks >= self.__10_bot_net_cost:
      self.__clicks -= self.__10_bot_net_cost
      self.__bot_nets += 10
    
  def __handleSellClicker(self):
    if self.__clickers >= 1:
      self.__clicks += self.__clicker_sell
      self.__clickers -= 1

  def __handleSell10Clickers(self):
    if self.__clickers >= 10:
      self.__clicks += self.__10_clicker_sell
      self.__clickers -= 10

  def __handleSellBotNet(self):
    if self.__bot_nets >= 1:
      self.__clicks += self.__bot_net_sell
      self.__bot_nets -= 1

  def __handleSell10BotNets(self):
    if self.__bot_nets >= 10:
      self.__clicks += self.__10_bot_net_sell
      self.__bot_nets -= 10

  def __click(self):
    self.__clicks += 1

  def __createTimer(time, function):
    dummy = Timer(time, function)
    dummy.start()

  def __updateAttributes(self):
    self.__calculateCosts()
    self.__calculateSells()

  def __calculateCosts(self):
    self.__clicker_cost = Clicker.__GROWTH_RATE ** (self.__clickers - 1) * Clicker.__BASE_CLICKER_COST
    self.__bot_net_cost = Clicker.__GROWTH_RATE ** (self.__bot_nets - 1) * Clicker.__BASE_BOT_NET_COST

    self.__10_clicker_cost = 0
    self.__10_bot_net_cost = 0
    
    for count in range(10):
      self.__10_clicker_cost += Clicker.__GROWTH_RATE ** (self.__clickers + count - 1) * Clicker.__BASE_CLICKER_COST
      self.__10_bot_net_cost += Clicker.__GROWTH_RATE ** (self.__bot_nets + count - 1) * Clicker.__BASE_BOT_NET_COST

  def __calculateSells(self):
    self.__clicker_sell = 0.75 * Clicker.__GROWTH_RATE ** (self.__clickers - 2) * Clicker.__BASE_CLICKER_COST
    self.__bot_net_sell = 0.75 * Clicker.__GROWTH_RATE ** (self.__bot_nets - 2) * Clicker.__BASE_BOT_NET_COST

    self.__10_clicker_sell = 0
    self.__10_bot_net_sell = 0
    
    for count in range(10):
      self.__10_clicker_sell += 0.75 * Clicker.__GROWTH_RATE ** (self.__clickers - count - 2) * Clicker.__BASE_CLICKER_COST
      self.__10_bot_net_sell += 0.75 * Clicker.__GROWTH_RATE ** (self.__bot_nets - count - 2) * Clicker.__BASE_BOT_NET_COST


if __name__ == "__main__":
  a = Clicker()
  a.run()