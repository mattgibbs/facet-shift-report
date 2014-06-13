class form_data(object):

    def __init__(self, form):
        self.usergroup = form['usergroup']
        self.shift = form['shift']
        self.personnel = form['personnel']
        self.goals = form['goals']
        self.progress = form['progress']
        self.problems = form['problems']
        self.next_shift = form['next_shift']
        self.brief_summary = form['brief_summary']
        self.other = form['other']
        self.useful_beam_time  = form['useful_beam_time']
        self.unscheduled_accelerator_down = form['unscheduled_accelerator_down']
        self.other_down_reason = form['other_down_reason']
        self.accelerator_physicist_availability = form['accelerator_physicist_availability']

    def get_tuple(self):
        return (self.usergroup, self.shift, self.personnel, self.goals, self.progress,
                self.problems, self.next_shift, self.brief_summary, self.other,
                self.useful_beam_time, self.unscheduled_accelerator_down,
                self.other_down_reason, self.accelerator_physicist_availability)

    def get_dict(self):
        dict_form = {}
        dict_form['usergroup'] = self.usergroup
        dict_form['shift'] = self.shift
        dict_form['personnel'] = self.personnel
        dict_form['goals'] = self.goals
        dict_form['progress'] = self.progress
        dict_form['problems'] = self.problems
        dict_form['next_shift'] = self.next_shift
        dict_form['brief_summary'] = self.brief_summary
        dict_form['other'] = self.other
        dict_form['useful_beam_time'] = self.useful_beam_time
        dict_form['unscheduled_accelerator_down'] = self.unscheduled_accelerator_down
        dict_form['other_down_reason'] = self.other_down_reason
        dict_form['accelerator_physicist_availability'] = self.accelerator_physicist_availability
        return dict_form