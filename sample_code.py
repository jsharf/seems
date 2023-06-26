import seems.seems as seems

@seems.ReturnValue().IsEven
@seems.ReturnValue().IsInteger
def Double(x: int) -> int:
    return int(x * 2)