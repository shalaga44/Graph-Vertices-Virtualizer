class MainDiments:
    scaleFactor = .9


class VerticesDiments:
    radius = int(25 * MainDiments.scaleFactor)
    fontSize = int(30 * MainDiments.scaleFactor)
    intersectionRadius = radius * 2


class EdgesDiments:
    width = 5
    length = VerticesDiments.intersectionRadius+10
