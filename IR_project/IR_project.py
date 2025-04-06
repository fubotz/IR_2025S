from collections import deque


class Step:
    """
    A Step represents a step in the Labyrinth, consisting of a row offset and a column offset
    """
    def __init__(self, row_offset, column_offset):
        self.row_offset = row_offset
        self.column_offset = column_offset


class Location:
    """
    Location represents a location in the labyrinth, it consists of the row and the column of the location it
    represents. We primarily use the Location class to represent a path in the labyrinth as a list of locations.

    It is hashable (__hash__ and __eq__) so that it can be put into sets (something we do in our bfs, where we add
    locations the visited set).

    It is comparable (__eq__) to other locations, a capability we need when we check whether our search arrived at
    the desired end location.

    In addition, it provides the + operator (the __add__ method, which we did not discuss in class. This is also a
    way of customizing a class in Python). In this implementation, the __add__ method allows us to add another
    location to this location and return the result as a new location (which is used in the bfs algorithm when we
    move a location according to one of the four directions).
    """

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __add__(self, other: 'Step'):
        return Location(self.row + other.row_offset, self.column + other.column_offset)

    def __eq__(self, other: 'Location'):
        return self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash((self.row, self.column))

    def __repr__(self):
        return f"[{self.row}/{self.column}]"


class Path(list[Location, ...]):
    """
    A Path represents a series of locations in the labyrinth represented as a list.

    A path offers some convenience methods, e.g. to get the locations at which it currently ends, and a method to extend
    itself with a given location.
    """

    def __init__(self, param):
        """If the given parameter is a location, it is wrapped in a list, else it is passed as is to the parent's
        initialization method.
        """
        super().__init__([param] if isinstance(param, Location) else param)

    def last(self) -> Location:
        """Returns the last location of this path
        :return: The location at which this path currently ends
        """
        return self[-1]

    def leads_to(self, end: Location):
        """Returns whether this path leads to the given location
        :param end: The location to check
        :return: Whether this path ends at the given location
        """
        return self.last() == end

    def extend(self, step: Step) -> 'Path':
        """Creates and returns a new path, which extends this path by taking a step into the given direction.
        :param step: The step in which we want to move the last location of the path
        :return: A new path, which extends this path
        """
        extended = Path(self)
        extended.append(extended.last() + step)
        return extended


class Labyrinth(list[str, ...]):
    """
    The Labyrinth represents a maze built from a list of strings.

    It can print itself including a path through the labyrinth, and it can search for a path that connects two locations
    using breadth-first search.
    """
    def __init__(self, maze: list[str, ...]):
        # Check whether all lines of the given maze have the same length and raise an error if they are not
        line_lengths = {len(line) for line in maze}
        if len(line_lengths) > 1:
            raise ValueError("The given maze has rows of different lengths. Please check.")

        super().__init__(maze)

    @staticmethod
    def replace_at_index(s: str, r: str, idx: int) -> str:
        """A static helper method to replace a string r at a given index idx in a string s"""
        return s[:idx] + r + s[idx + len(r):]

    @staticmethod
    def create_row_headers(length):
        """A static helper method to create the headers when printing the labyrinth"""
        return "".join(str(i % 10) for i in range(length))

    def get_width(self):
        """Returns the width of the labyrinth"""
        return len(self[0])

    def print(self, path: Path = None):
        """
        Prints the labyrinth, and, optionally, a path within it
        :param path: A path, that, when given, is marked with 'X's while printing the labyrinth
        """
        headers = Labyrinth.create_row_headers(self.get_width())

        print(" ", headers, sep="")

        # enumerate gives us the index and the value at the index
        for row, line in enumerate(self):
            # We have a path, e.g., it is not None
            if path:
                # We iterate all the elements of the path. These are locations
                for location in path:
                    if location.row == row:
                        # Here you can call the replace function to replace a white space with an "X", for example
                        line = Labyrinth.replace_at_index(line, "X", location.column)

            print(row % 10, line, row % 10, sep="")

        print(" ", headers, sep="")

    def is_traversable(self, location: Location) -> bool:
        """Checks whether the given location is in fact traversable, e.g., a space character"""
        return self[location.row][location.column] == " "

    def search_path_using_bfs(self, start: Location, end: Location) -> Path:
        """
        Offers breadth-first search for a path connecting the given locations start and end. Returns the path, if one
        is found
        :param start: The start location
        :param end: The end location
        :return: The path between the start and end location
        """
        # Our queue which will hold paths that we already considered in our search
        queue = deque[Path]()
        # We start with the path that solely consists of our start location
        queue.append(Path(start))

        # A set of visited locations, that helps us to avoid testing the same location twice
        visited = set[Location]()

        # Create the list of possible steps as a list of locations
        steps = [Step(offset[0], offset[1]) for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]]

        while queue:
            # We get the first path from our queue of paths
            path = queue.popleft()

            # Return the path if it leads to the desired end location
            if path.leads_to(end):
                return path

            # If the last location of the path was not visited yet, visit it
            if path.last() not in visited:
                # Prevent the last location of the current path from being visited again by adding it to set of visited
                # locations
                visited.add(path.last())

                # Test the steps in all four directions
                for step in steps:
                    # Extend the current path with the step
                    new_path = path.extend(step)
                    # If the last location of the extended path is traversable, add the extended path to the queue
                    if self.is_traversable(new_path.last()):
                        queue.append(new_path)


def prompt_integer(message: str) -> int:
    """
    Prompts the user for an integer using the given message. If the given input is not an integer, the user is
    prompted again
    :param message: The message to prompt the user with
    :return: The integer given by the user
    """
    while True:
        given = input(message + ": ")
        if given.isdigit():
            return int(given)
        print(f"'{given} is not an integer, try again ;)")


def prompt_user_for_location(location_name: str) -> Location:
    """
    Prompts the user for a location, that is, a row and a column, with the given name
    :param location_name: The name to prompt with
    :return: The location given by the user
    """
    row = prompt_integer("Row of " + location_name)
    column = prompt_integer("Column of " + location_name)
    return Location(row, column)


# Create the labyrinth
labyrinth = Labyrinth([
            "███████",
            "█     █",
            "█   ███",
            "█ ███ █",
            "█     █",
            "███████"
        ])

# Print the labyrinth to the user to make choosing the start and end locations easier
labyrinth.print()

# Prompt the user for start and end locations
start_location = prompt_user_for_location("start")
end_location = prompt_user_for_location("end")

# Search for a path connecting the given locations
path_found = labyrinth.search_path_using_bfs(start_location, end_location)

if not path_found:
    print("No path found...")
else:
    # Print the labyrinth again including the path found
    labyrinth.print(path_found)
