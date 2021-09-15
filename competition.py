#
# Copyright (C) 2017 Tignis, Inc.
#

"""
Implement the Competition class.
"""

import math
from decimal import Decimal


def round_value(value, precision=Decimal('1.000')):
    """
    Round float value to specified precision.

    :param value: Float value.
    :param precision: Precision as a Decimal() object.
    :return: Rounded float value.
    """
    return float(Decimal(value).quantize(precision))


# TODO: Implement this class to simulate the competition.
class Competition(object):
    """
    Simulation of a hot dog eating competition.
    """

    def __init__(self, competitors, duration):
        """
        Initialize the competition.

        :param competitors: A dictionary of {competitor name: hot dog function}.
        :param duration: Duration in seconds of the competition.
        """
        self.competitors = competitors
        self.duration = duration
        self.event_list = list()  # Store events

    def run(self):
        """
        Run a simulation of the competition and return a list of Events. Events should be sorted by elapsed_time
        first, then name if they have the same elapsed_time. There should be an Event for every whole hot dog that is
        eaten by a competitor, as well as an Event for each competitor at the end of the competition. See the
        expected results file for each testcase.

        :return: List of (or iterator over) Events.
        """
        cnt = 0  # Counter for loop
        durations = dict()  # {"Joey": 5.0, "Carmen": 6.0}  -> {"Joey": 10.035, "Carmen": 12.12}
        breaks = dict()  # [0, 0, ... 0] -> [1, 1, ... 1], if all elements equal 1, break the loop
        # Initialize breaks
        for competitor in self.competitors:
            breaks[competitor] = 0
        while 1:
            # Calculate the current eaten time and next eaten time for hot dogs for every competitors.
            # Then compute total durations and decide to break the loop or not.
            for competitor in self.competitors:
                if not breaks[competitor]:  # If breaks[competitor] == 1, it means this competitor is out of time.
                    current_eaten_time = self.competitors[competitor](cnt)
                    next_eaten_time = self.competitors[competitor](cnt + 1)
                    # Calculate the elapsed time for this competitor
                    if competitor in durations:
                        durations[competitor] += current_eaten_time
                    else:
                        durations[competitor] = current_eaten_time
                    event = Event(durations[competitor], competitor, float(cnt + 1))  # Define the current event
                    self.event_list.append(event)
                    # If duration of the competition - elapsed time - next eaten time <=0,
                    # it means there will be no next loop and we should calculate the eaten percent of next hot dog.
                    diff = self.duration - durations[competitor] - next_eaten_time
                    if diff < 0:
                        breaks[competitor] = 1
                        # duration_left is the left time and must be less than next_eaten_time
                        duration_left = self.duration - durations[competitor]
                        # current hot_dog_eaten == cnt + 1,
                        # so total hot dog = current hot dog + time left / next eaten time
                        total_hot_dog_eaten = round_value(cnt + 1 + duration_left / next_eaten_time, Decimal('1.00'))
                        event = Event(self.duration, competitor, total_hot_dog_eaten)
                        self.event_list.append(event)
            cnt += 1
            is_break = True if sum(breaks.values()) == len(breaks) else False  # e.g. [1, 1] => 2 == 2, [1, 0] => 1 != 2
            if is_break:
                break
        self.event_list.sort()  # Sort the list as required, and we can use sort directly because of __lt__ method
        # After the list is sorted with the precise values, it can be rounded and returned
        result_event_list = list(map(lambda x: x.rounded(), self.event_list))
        return result_event_list

    def winner(self):
        """
        Get the winner of the competition. If multiple competitors have eaten the same number of hot dogs,
        the competitor whose name comes first lexicographically is the winner.

        :return: Name of winner.
        """
        return max(self.event_list).name  # __lt__


class Event(object):
    """
    An Event should be generated whenever a hot dog is eaten by a competitor, and at the end of the competition for
    each competitor.
    """

    def __init__(self, elapsed_time, name, total_hot_dogs_eaten):
        self.elapsed_time = elapsed_time
        self.name = name
        self.total_hot_dogs_eaten = total_hot_dogs_eaten

    def __repr__(self):
        return 'Event(elapsed_time=%s, name=%s, total_hot_dogs_eaten=%s)' % (
            repr(self.elapsed_time), repr(self.name), repr(self.total_hot_dogs_eaten))

    def __eq__(self, other):
        """
        Whether two Events can be considered to be identical.

        :param other: The other Event.
        :return: True if the Events are identical.
        """
        return (
            self.elapsed_time == other.elapsed_time and
            self.name == other.name and
            self.total_hot_dogs_eaten == other.total_hot_dogs_eaten
        )

    def __lt__(self, other):
        """
        If two Events occur at the same time, sort them alphabetically by competitor name.

        :param other: The other Event.
        :return: True if this Event should come before the other Event.
        """
        if self.elapsed_time == other.elapsed_time:
            return self.name < other.name
        else:
            return self.elapsed_time < other.elapsed_time

    def rounded(self, precision=Decimal('1.000')):
        """
        Round numeric fields to 3 decimal points.

        :return: New Event with numeric fields rounded to 3 decimal points.
        """
        return Event(round_value(self.elapsed_time, precision),
                     self.name,
                     round_value(self.total_hot_dogs_eaten, precision))


if __name__ == '__main__':
    testcases = {
                    'competitors': {
                        'Joey Chestnut': lambda n: math.exp(0.0344 * n) + 4,
                        'Carmen Cincotti': lambda n: n * 0.120 + 6,
                    },
                    'duration': 600,
                    'results': '2017.json',
                    'name': '2017',
                }
    c = Competition(testcases["competitors"], testcases["duration"])
    c.run()
    print(c.winner())
