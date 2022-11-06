class WebSearchResult:
    """
        Class the will store the 
        values of the results
    """

    title: str = ""
    price: str = ""
    delivery: str = ""

    def __init__(self, title, price, delivery):
        self.title = title
        self.price = price
        self.delivery = delivery