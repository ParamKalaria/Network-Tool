import pyfiglet
from colorama import Fore, Style
import main



big_text = Fore.CYAN + Style.BRIGHT + pyfiglet.figlet_format("Network Tool")


small_text = Fore.YELLOW + Style.BRIGHT + "by Param Kalaria" + Style.RESET_ALL


print(big_text + '\n' + small_text)
print(Fore.CYAN + Style.BRIGHT + "Welcome to the Network Tool!" + Style.RESET_ALL)

main.task_select()