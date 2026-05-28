def bottles_of_beer(bob):
    if bob < 1:
        print("""Нет бутылок пива на стене.
Нет бутылок пива.""")
        return
    tmp = bob
    bob -= 1
    print("""{} бутылок пива на стене. {} бутылок пива.
Возьми одну, пусти по кругу, {} бутылок пива на стене.
          """.format(tmp,
                     tmp,
                     bob))
    bottles_of_beer(bob)


bottles_of_beer(99)