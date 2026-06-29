class Trade:

    total_trades = 0
    winning_trades = 0
    break_even_trades = 0
    losing_trades = 0
    total_profit = 0
    
    

    def __init__(self, pair, entry, exit):
        
        self.pair = pair
        self.entry = entry
        self.exit = exit
        Trade.total_trades += 1

        self.net_gain = self.exit - self.entry

        if self.net_gain > 0:
            Trade.winning_trades += 1
            Trade.total_profit += self.net_gain
        elif self.net_gain < 0:
            Trade.losing_trades += 1
        

    def profit(self):
        return f'Net gain:{self.exit - self.entry}'
    
    
    def result(self):

        if self.net_gain > 0:
            return 'Profit'
        elif self.net_gain < 0:
            return 'Loss'
        return 'Break Even'
    

class TradeJournal(Trade):

    all_trades = []
    profitable_trades_dict = {}
    losing_trades_dict = {}
    best_pair = ''
    best_profit = 0
    worst_pair = ''
    worst_loss = 0
    avg_profit = 0
    win_rate = 0
    win_avg = 0

    def __init__(self, pair, entry, exit):
        
        super().__init__(pair, entry, exit)

        self.trade_entry = f'{self.pair}:- Entry: {self.entry} Exit: {self.exit}, Result: {self.result()}'
        TradeJournal.all_trades.append(self.trade_entry)

        if self.net_gain > 0:
            TradeJournal.profitable_trades_dict.update({self.pair : self.net_gain} )

            if self.net_gain > TradeJournal.best_profit:
                TradeJournal.best_profit = self.net_gain
                TradeJournal.best_pair = self.pair
        
        elif self.net_gain < 0:
            TradeJournal.losing_trades_dict.update({self.pair : self.net_gain})

            if self.net_gain < TradeJournal.worst_loss:
                TradeJournal.worst_pair = self.pair
                TradeJournal.worst_loss = self.net_gain
        else:
            Trade.break_even_trades += 1
        
    
    @classmethod
    def show_all_trades(cls):
        return cls.all_trades 
    
    @classmethod
    def statistics(cls):

        
        if cls.total_trades == 0:
            raise ValueError ('No winning trades yet')
        cls.win_rate = (cls.winning_trades / cls.total_trades)*100


        try:

            if cls.winning_trades == 0:
                raise Exception
            elif cls.winning_trades > 0:
                cls.avg_profit = cls.total_profit / cls.winning_trades
        except Exception as e:
            print(e)

        return (f'''
        Total trades: {cls.total_trades}
        Winning trades: {cls.winning_trades}
        Break Even trades: {cls.break_even_trades}
        Losing trades: {cls.losing_trades}
        Win Rate: {cls.win_rate:.2f}%
        Average Profit: {cls.avg_profit:.2f}
        Best trade: '{cls.best_pair}' - Profit: {cls.best_profit}
        Worst trade: '{cls.worst_pair}' - Loss: {cls.worst_loss}\n''')


from ast import literal_eval

def fetch_trades():
    final_trade_list = []

    try:
        with open('journal.txt', 'r') as rf:
            for line in rf:
                if ': ' not in line:
                    continue
                tuple_string = line.split(': ', 1)[1]
                trade = literal_eval(tuple_string)
                final_trade_list.append(trade)
    except FileNotFoundError:
        print("No journal file found. Save some trades first.")

    return final_trade_list


trade_counter = 0

for pair, entry, exit in fetch_trades():   

    trade_counter += 1
    try:     
        if entry < 0 or exit < 0:
            raise Exception

        trade  = TradeJournal(pair, entry, exit)
        
    except Exception as e:
        print(f'Trade no: {trade_counter}:- [({pair}), ({entry}), ({exit})] has invalid value/s')



lst = []

def add_trade(p, en, ex):

    t = (p.capitalize(), en, ex)
    lst.append(t)
    trade = TradeJournal(p.capitalize(), en, ex)
    print(f"Trade added: {trade.trade_entry}")
    

def save_to_journal(lst):

    try:
        with open('journal.txt', 'r') as rf:
            counter = len(rf.readlines())
    except FileNotFoundError:
        counter = 0

    with open('journal.txt', 'a') as af:
        
        for trade in lst:
            af.write(f'Trade {counter}: {trade}\n')
            counter += 1



while True:

        print("""
===== Trade Journal =====

1. Add Trade
2. Show All Trades
3. Show Statistics
4. Exit
""")
        
        choice = input('Choose option: ')

        if choice == '1':

            try:  

                pair = input('Pair: ')
                entry = int(input('Entry: '))
                exit = int(input('Exit: '))
                
                 
                if entry < 0 or exit < 0:
                    raise Exception
                
                add_trade(pair, entry, exit)

                save_choice = input('Do you want to save the trade? [y/n]: ')
                if save_choice.lower() == 'y':
                    save_to_journal(lst)
                    lst.clear()
                    print('Trade saved...\n')
                else:
                    print('Trade not saved\n')
        
            except Exception as e:
                print(f'Trade no: {trade_counter}:- [({pair}), ({entry}), ({exit})] has invalid value/s\n')
                
             
        elif choice == '2':   
            all_trades = TradeJournal.show_all_trades()
            if not all_trades:
                print("No trades yet.\n")
            else:
                for trade in all_trades:
                    print(trade)
        
        elif choice == '3':
            print(TradeJournal.statistics())
    
        elif choice == '4':
            break
        else:
            print('Invalid Option\n')
        
        print('Run code again for further operations:')
        break

