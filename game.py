# Check for special variables__ name__ , which is set during program execution. If the file is executed as the main program, the variable is set to '0'__ main__ '; if this file is imported by the test framework, the variable will not be'__ main__ '

import  alien_invasion as av

ai = av.AlienInvasion()
ai.run_game()