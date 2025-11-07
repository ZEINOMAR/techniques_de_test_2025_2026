def triangulate(points):
    if len(points) < 3:
        raise ValueError("Moins de 3 points: non triangulable.")
    return [(0, 1, 2)]
