"""US bank holidays"""
import holidays


class USBankHolidays(holidays.UnitedStates):
    def _populate(self, year):
        super()._populate(year)

        self.pop_named("Columbus Day")
        self.pop_named("Veterans Day")
