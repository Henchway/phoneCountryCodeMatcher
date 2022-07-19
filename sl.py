# Import the interface required by the Script snap.
from com.snaplogic.scripting.language import ScriptHook


class TransformScript(ScriptHook):
    def __init__(self, input, output, error, log):
        self.input = input
        self.output = output
        self.error = error
        self.log = log

    def match(self, input_number, country_codes, current_slice=5):
        """ Returns the number (without prefix) and the matched country"""
        input_number = input_number.replace(" ", "")
        if current_slice == 0:
            return None
        part = input_number[0:current_slice]
        if part in country_codes.keys():
            return input_number[len(part):], country_codes[part]
        return self.match(input_number, country_codes=country_codes, current_slice=(current_slice - 1))

    # The "execute()" method is called once when the pipeline is started
    # and allowed to process its inputs or just send data to its outputs.
    def execute(self):
        self.log.info("Executing Transform script")
        while self.input.hasNext():
            try:
                # Read the next input document, store it in a new dictionary, and write this as an output document.
                inDoc = self.input.next()
                number = inDoc['mobile']
                codes = inDoc['codes']
                cleaned_number, code = self.match(number, codes)

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
