# Import the interface required by the Script snap.
from com.snaplogic.scripting.language import ScriptHook


class TransformScript(ScriptHook):
    def __init__(self, input, output, error, log):
        self.input = input
        self.output = output
        self.error = error
        self.log = log

    def match(self, input_number, country_codes, country, current_slice=5):
        """ Returns the number (without prefix) and the matched country"""
        if input_number is None:
            return None, None
        input_number = input_number.replace(" ", "").replace("-", "")
        if current_slice == 0:
            return None, None
        part = input_number[0:current_slice]
        if part in country_codes.keys():
            country_code = [x['ID'] for x in country_codes[part] if x['2dig'] == country]
            if len(country_code) == 0 and len(country_codes[part]) != 0:
                country_code = [x['ID'] for x in country_codes[part]]
            if country_code:
                return input_number[len(part):], country_code.pop(0)
            else:
                return None, None
        return self.match(input_number, country_codes=country_codes, current_slice=current_slice - 1, country=country)

    # The "execute()" method is called once when the pipeline is started
    # and allowed to process its inputs or just send data to its outputs.
    def execute(self):
        self.log.info("Executing Transform script")
        while self.input.hasNext():
            try:
                # Read the next input document, store it in a new dictionary, and write this as an output document.
                inDoc = self.input.next()
                number = inDoc['mobile']
                country = inDoc['country']
                codes = inDoc['codes']
                cleaned_number, code = self.match(number, codes, country)

                outDoc = {
                    'original': inDoc,
                    'cleaned_number': cleaned_number,
                    'code': code
                }
                self.output.write(inDoc, outDoc)
            except Exception as e:
                errDoc = {
                    'error': str(e)
                }
                self.log.error("Error in python script")
                self.error.write(errDoc)

        self.log.info("Script executed")

    # The "cleanup()" method is called after the snap has exited the execute() method
    def cleanup(self):
        self.log.info("Cleaning up")


# The Script Snap will look for a ScriptHook object in the "hook"
# variable.  The snap will then call the hook's "execute" method.
hook = TransformScript(input, output, error, log)
