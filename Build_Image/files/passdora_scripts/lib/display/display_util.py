from lib.display.lcddriver import lcd

class Display:
    LCD = lcd()

    def show(self, line1, line2):
        self.LCD.display_string("--==| PASSDORA |==--", 0)
        self.LCD.display_string("|{0}|".format(line1.center(18)), 1)
        self.LCD.display_string("|{0}|".format(line2.center(18)), 2)
        self.LCD.display_string("--------------------", 3)
    
    def clear(self):
        self.LCD.clear()

