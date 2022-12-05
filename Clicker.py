from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from sys import exit

from math import floor, ceil, log


class Clicker(App):

  __BASE_CLICKER_COST = 10
  __BASE_BOT_NET_COST = 100
  __COST_CHANGER = 1.5 # Due to the logarithms base this constant, lowering *increases* rate of growth
  __CLICKER_COUNTER_MAX = 1
  __BOT_NET_COUNTER_MAX = 20/3


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

    self.__clicker_counter = Clicker.__CLICKER_COUNTER_MAX
    self.__bot_net_counter = Clicker.__BOT_NET_COUNTER_MAX

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

    self.__button_associations = {
      self.__main_button:self.handleMainButton,
      self.__buy_clicker_button:self.handleBuyClicker,
      self.__buy_10_clicker_button:self.handleBuy10Clickers,
      self.__sell_clicker_button:self.handleSellClicker,
      self.__sell_10_clicker_button:self.handleSell10Clickers,
      self.__buy_bot_net_button:self.handleBuyBotNet,
      self.__buy_10_bot_net_button:self.handleBuy10BotNets,
      self.__sell_bot_net_button:self.handleSellBotNet,
      self.__sell_10_bot_net_button:self.handleSell10BotNets,
      }

    for button in self.__button_associations:
      button.bind(on_press=self.__button_associations[button])

    
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

  def mainLoop(self, delta):
    self.__updateAttributes()
    self.__updateLabels()
    self.__clicker_counter -= delta
    if self.__clicker_counter <= 0:
      self.__clicks += self.__clickers
      self.__clicker_counter = Clicker.__CLICKER_COUNTER_MAX
    self.__bot_net_counter -= delta
    if self.__bot_net_counter <= 0:
      self.__clicks += self.__bot_nets * 10
      self.__bot_net_counter = Clicker.__BOT_NET_COUNTER_MAX

  def __updateLabels(self):
    self.__main_button.text = str(self.__clicks)
    self.__clickers_label.text = "Clickers: " + str(self.__clickers)
    self.__bot_nets_label.text = "Bot Nets: " + str(self.__bot_nets)
    self.__buy_clicker_button.text = "Buy 1: " + str(self.__clicker_cost)
    self.__buy_10_clicker_button.text = "Buy 10: " + str(self.__10_clicker_cost)
    self.__sell_clicker_button.text = "Sell 1: " + str(self.__clicker_sell)
    self.__sell_10_clicker_button.text = "Sell 10: " + str(self.__10_clicker_sell)
    self.__buy_bot_net_button.text = "Buy 1: " + str(self.__bot_net_cost)
    self.__buy_10_bot_net_button.text = "Buy 10: " + str(self.__10_bot_net_cost)
    self.__sell_bot_net_button.text = "Sell 1: " + str(self.__bot_net_sell)
    self.__sell_10_bot_net_button.text = "Sell 10: " + str(self.__10_bot_net_sell)

  def handleMainButton(self, button):
    self.__clicks += 1

  def handleBuyClicker(self, button):
    if self.__clicks >= self.__clicker_cost:
      self.__clicks -= self.__clicker_cost
      self.__clickers += 1

  def handleBuy10Clickers(self, button):
    if self.__clicks >= self.__10_clicker_cost:
      self.__clicks -= self.__10_clicker_cost
      self.__clickers += 10

  def handleBuyBotNet(self, button):
    if self.__clicks >= self.__bot_net_cost:
      self.__clicks -= self.__bot_net_cost
      self.__bot_nets += 1

  def handleBuy10BotNets(self, button):
    if self.__clicks >= self.__10_bot_net_cost:
      self.__clicks -= self.__10_bot_net_cost
      self.__bot_nets += 10
    
  def handleSellClicker(self, button):
    if self.__clickers >= 1:
      self.__clicks += self.__clicker_sell
      self.__clickers -= 1

  def handleSell10Clickers(self, button):
    if self.__clickers >= 10:
      self.__clicks += self.__10_clicker_sell
      self.__clickers -= 10

  def handleSellBotNet(self, button):
    if self.__bot_nets >= 1:
      self.__clicks += self.__bot_net_sell
      self.__bot_nets -= 1

  def handleSell10BotNets(self, button):
    if self.__bot_nets >= 10:
      self.__clicks += self.__10_bot_net_sell
      self.__bot_nets -= 10

  def __updateAttributes(self):
    self.__calculateCosts()
    self.__calculateSells()


  # Current formula: nth clicker costs 1.5^(n-1) * 10
  # New suggested formula: nth clicker costs (0.2 log1.5(x) + 1) * 10

  def __calculateCosts(self):
    #self.__clicker_cost = floor(Clicker.__COST_CHANGER ** (self.__clickers) * Clicker.__BASE_CLICKER_COST)
    #self.__bot_net_cost = floor(Clicker.__COST_CHANGER ** (self.__bot_nets) * Clicker.__BASE_BOT_NET_COST)

    c = Clicker.__COST_CHANGER
    x = self.__clickers + 1 # +1 creates one to buy
    y = self.__bot_nets + 1

    self.__clicker_cost = floor((0.2*x*log(x,c)+1) * Clicker.__BASE_CLICKER_COST)
    self.__bot_net_cost = floor((0.2*y*log(y,c)+1) * Clicker.__BASE_BOT_NET_COST)

    self.__10_clicker_cost = 0
    self.__10_bot_net_cost = 0

    for count in range(10):
      self.__10_clicker_cost += (0.2*x*log(x+count,c)+1) * Clicker.__BASE_CLICKER_COST
      self.__10_bot_net_cost += (0.2*y*log(y+count,c)+1) * Clicker.__BASE_BOT_NET_COST

    self.__10_clicker_cost = floor(self.__10_clicker_cost)
    self.__10_bot_net_cost = floor(self.__10_bot_net_cost)

  def __calculateSells(self):

    c = Clicker.__COST_CHANGER
    x = self.__clickers
    y = self.__bot_nets


    try:
      self.__clicker_sell = ceil(0.75 * (0.2*x*log(x,c)+1) * Clicker.__BASE_CLICKER_COST)
    except ValueError:
      self.__clicker_sell = "N/A"
    try:
      self.__bot_net_sell = ceil(0.75 * (0.2*y*log(y,c)+1) * Clicker.__BASE_BOT_NET_COST)
    except ValueError:
      self.__bot_net_sell = "N/A"

    self.__10_clicker_sell = 0
    self.__10_bot_net_sell = 0
    
    for count in range(10):
      try:
        self.__10_clicker_sell += ceil(0.75 * (0.2*x*log(x-count,c)+1) * Clicker.__BASE_CLICKER_COST)
      except ValueError:
        self.__10_clicker_sell = "N/A"
      try:
        self.__10_bot_net_sell += ceil(0.75 * (0.2*y*log(y-count,c)+1) * Clicker.__BASE_BOT_NET_COST)
      except ValueError:
        self.__10_bot_net_sell = "N/A"

if __name__ == "__main__":
  a = Clicker()
  a.run()
  exit(0)