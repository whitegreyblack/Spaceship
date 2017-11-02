import random

class Color:
    """Color class used as a static method to import hexvalue color codes"""

    # GREYS
    white = "#FFFFFF"
    grey_lightest = "#FAFCFC"
    grey_lighter = "#F3F7F9"
    grey_light = "#DAE4E9"
    grey = "#9BABB4"
    grey_dark = "#70818A"
    grey_darker = "#596A73"
    grey_darkest = "#364349"
    black = "#222B2F"
    
    # RED
    red_lightest = "#FCEBEA"
    red_lighter = "#F9ACAA"
    red_light = "#EF5753"
    red = "#E3342F"
    red_dark = "#CC1F1A"
    red_darker = "#CA1B19"
    red_darkest = "#420806"

    # ORANGE
    orange_lightest = "#FFF5EB"
    orange_lighter = "#FCD9B6"
    orange_light = "#FAAD63"
    orange = "#F6993F"
    orange_dark = "#DE751F"
    orange_darker = "#7F4012"
    orange_darkest = "#542605"

    # YELLOW
    yellow_lightest = "#FCFBEB"
    yellow_lighter = "#FFF9C2"
    yellow_light = "#FFF382"
    yellow = "#FFED4A"
    yellow_dark = "#F2D024"
    yellow_darker = "#684F1D"
    yellow_darkest = "#453411"

    # GREEN
    green_lightest = "#E3FCEC"
    green_lighter = "#A2F5BF"
    green_light = "#51D88A"
    green = "#38C172"
    green_dark = "#1F9D55"
    green_darker = "#0B4228"
    green_darkest = "#032D19"

    # TEAL
    teal_lightest = "#E8FFFE"
    teal_lighter = "#A0F0ED"
    teal_light = "#64D5CA"
    teal = "#4DC0B5"
    teal_dark = "#38A89D"
    teal_darker = "#174E4B"
    teal_darkest = "#0D3331"

    # BLUE
    blue_lightest = "#EFF8FF"
    blue_lighter = "#BCDEFA"
    blue_light = "#6CB2EB"
    blue = "#3490DC"
    blue_dark = "#2779BD"
    blue_darker = "#103D60"
    blue_darkest = "#05233B"

    # INDIGO
    indigo_lightest = "#E6E8FF"
    indigo_lighter = "#B2B7FF"
    indigo_light = "#7886D7"
    indigo = "#6574CD"
    indigo_dark = "#5661B3"
    indigo_darker = "#2F365F"
    indigo_darkest = "#191E38"

    # PURPLE
    purple_lightest = "#F3EBFF"
    purple_lighter = "#D6BBFC"
    purple_light = "#A779E9"
    purple = "#9561E2"
    purple_dark = "#794ACF"
    purple_darker = "#352465"
    purple_darkest = "#1F133F"

    # PINK
    pink_lightest = "#FFEBEF"
    pink_lighter = "#FFBBCA"
    pink_light = "#FA7EA8"
    pink = "#F66D9B"
    pink_dark = "#EB5286"
    pink_darker = "#72173A"
    pink_darkest = "#45051E"

    @classmethod
    def color(cls, col: str) -> str:
        '''Returns the hex value of a given color
        
        Example:
            >>> Color.color('red')
            #E3342F
            >>> Color.color('red.lighter)
            #F0ACAA
        '''
        if "." in col:
            col = col.replace('.', "_")
        if hasattr(cls, col):
            return getattr(cls, col)
        raise AttributeError("No hexcode for the given color")

    @classmethod
    def color_rgb(cls, col:str) -> str:
        '''Returns the rgb value of a given color
    
        Example:
            >>> Color.color('red')
            (14, 3, 2)
            >>> Color.color('red.lighter)
            (15, 10, 10)        
            '''
        hexval = cls.color(col)
        return int(hexval[1:3], 16), int(hexval[3:5], 16), int(hexval[5:7], 16)

if __name__ == "__main__":
    print(Color.color('red'))
    print(Color.color('red.lighter'))
    print(Color.color('blue'))
    print(Color.color_rgb('red'))
    print(Color.color_rgb('red.lighter'))