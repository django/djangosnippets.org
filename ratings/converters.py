class FloatConverter:
    regex = "-?([0-9]*[.])?[0-9]"

    def to_python(self, value):
        return "." in value and float(value) or int(value)

    def to_url(self, value):
        return str(value)
