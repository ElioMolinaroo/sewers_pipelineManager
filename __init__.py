"""----------------------------------------------------------------------------
--------------      Sewers Pipeline Manager by Elio Molinaro     --------------
----------------------------------------------------------------------------"""

__author__ = 'Elio Molinaro'
__version__ = (2, 0, 0)

from ui.uiView import startUI


def titleSewersCLI():
    print()
    print('-------------------------------------------------------------------------------')
    print(f'---------     Sewers Pipeline Manager v{__version__} by {__author__}     ---------')
    print('-------------------------------------------------------------------------------')
    print()


if __name__ == '__main__':
    # Shows the title of the window at the top of the terminal
    titleSewersCLI()
    # Starts the UI
    startUI()
