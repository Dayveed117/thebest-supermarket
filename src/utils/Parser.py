"""
Parser module for 'TheBest' supermarket transactions
"""

class Parser():
    """
    Parser class for parsing text files
    """

    @classmethod
    def parse_receipt(cls, linelist : 'list[str]') -> dict:

        products = []
        NIF      = 0
        TOTAL    = 0.0

        for line_ in linelist:
            line = line_.lstrip().rstrip()

            # Store NIF
            if line.startswith('Client'):
                (_, _,v) = line.split(' ', maxsplit=2)
                NIF = int(v)

            # Store every product in receipt
            elif line.startswith('>'):
                tmp = line.split(':', maxsplit=1)[0]
                p = tmp.split('>', maxsplit=1)[1].lstrip()
                products.append(p)

            # Store total value
            elif line.startswith('Total'):
                (_, tmp) = line.split(':')
                total = tmp.lstrip().rstrip().split(' ', maxsplit=1)[0]
                TOTAL = float(total)

            else:
                pass

        # First line with '>' is not needed
        products.pop(0)

        d = {
            'NIF'     : NIF,
            'TOTAL'   : TOTAL,
            'Products': products
        }

        return d

    @classmethod
    def parse_explanation(cls, linelist : 'list[str]') -> dict:

        # region LINES TACTICS
        # Split by lines by
        #  -
        # I bought the product | .
        #   | ...
        # Walking
        # Nearby there was  | ,
        # Nearby I looked and liked of  | .
        # endregion

        wishlist = []
        random_p = []
        stamina  = 0.0
        stamflag = False

        for line_ in linelist:
            line = line_.lstrip()

            # Wishlist products
            if line.startswith('-'):
                # from 3rd caracter to 2nd to 2nd last
                wishlist.append(line[2:-2])

            elif line.startswith('Nearby I'):
                # Split on 'of', get from 1st to 11th from last
                tmp = line.split('of', maxsplit=1)[1]
                r = tmp[1:-12]
                random_p.append(r)

            # Walked
            elif line.startswith('Walke') and not stamflag:
                # Split com espaço max 4
                _,wt,_,_,r = line.split(' ', maxsplit=4)
                w = wt.rstrip('.')
                stamina  = float(w) + float(r)
                stamflag = True

            else:
                pass

        # Dictionary that englobes data
        wishlist.reverse()
        d = {
          'STAMINA'        : stamina,
          'Wishlist'       : wishlist,
          'Random Products': random_p
        }

        return d
