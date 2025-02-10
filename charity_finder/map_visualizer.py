import folium
from folium.plugins import HeatMap
from typing import List, Final, Tuple, Optional
from django.db.models import QuerySet
from charity_finder.models import Project


class ProjectMapVisualizer:
    """
    Generates a Folium map with heat points and popups representing projects in need of funding.
    Attributes are set as constants and can be updated by developers to adjust the map's appearance.
    """

    # These values are considered constant throughout the program's execution but can be
    # updated by developers as necessary to reflect changes in requirements or configurations.
    INITIAL_LOCATION: Final[Tuple[float, float]] = (
        59.09827437369457,
        13.115860356662202,
    )  # Default map center
    ZOOM_START: Final[int] = 3  # Default zoom level
    IFRAME_WIDTH: Final[int] = 200  # Width of the iframe in pixels
    IFRAME_HEIGHT: Final[int] = 100  # Height of the iframe in pixels
    POPUP_MAX_WIDTH: Final[int] = 200  # Maximum width of the popup in pixels

    # HTML template for displaying project details in popups, with placeholders for project data.
    HTML_TEMPLATE: Final[
        str
    ] = """
        <b>Project Title:</b> {title}<br>
        <a href="{link}" target="_blank" rel="noopener noreferrer">Project Link</a><br>
        <b>Funding Needed:</b> {goal_remaining}<br>
        <b>Funding Weight:</b> {goal_norm}
    """

    def __init__(
        self,
        initial_location: Optional[Tuple[float, float]] = None,
        zoom_start: int = ZOOM_START,
    ):
        """
        Initializes a new ProjectMapVisualizer instance with an empty folium Map,
        centered at a specified location with a given zoom level. The `project_map`
        attribute stores the Folium map instance, which can be accessed directly to
        retrieve or modify the map.

        The map starts with no data (empty) and uses default values for its initial
        location and zoom level unless specified otherwise. Project data can be
        added to the map using other methods of this class.

        Args:
            initial_location: The center point of the map. Uses INITIAL_LOCATION if not provided,
                            allowing customization of the starting location.
            zoom_start: The initial zoom level of the map. Uses ZOOM_START if not provided,
                        allowing customization of the starting zoom level.
        """
        if initial_location is None:
            initial_location = self.INITIAL_LOCATION
        self.project_map = folium.Map(location=initial_location, zoom_start=zoom_start)

    def add_heat_points_and_popups(
        self, projects: QuerySet[Project], goal_remaining_max: float
    ) -> None:
        """
        Adds heat points based on projects' funding needs and popups with project details to the map.

        Args:
            projects: A collection of Project instances to visualize.
            goal_remaining_max: The maximum 'goal_remaining' value among all projects for normalization.

        Projects with valid map data are visualized with a heat point that varies in intensity based on
        the project's normalized funding need. Popups contain the project's title, a link, and its funding needs.
        """
        for project in projects:
            if project.has_map_data:
                # Normalizing the goal_remaining value for the heat map
                goal_norm = float(project.goal_remaining / goal_remaining_max)
                # Creating a list of latitude, longitude, and normalized goal_remaining for the heat point data
                heat_map_data = [
                    [int(project.latitude), int(project.longitude), goal_norm]
                ]
                # Adding heat point data to the map
                HeatMap(heat_map_data).add_to(self.project_map)

                # Using the template for HTML content
                html = self.HTML_TEMPLATE.format(
                    title=project.title,
                    link=project.project_link,
                    goal_remaining=int(project.goal_remaining),
                    goal_norm=goal_norm,
                )

                # Creating an iframe with the HTML content and adding it as a popup to the map
                iframe = folium.IFrame(
                    html, width=self.IFRAME_WIDTH, height=self.IFRAME_HEIGHT
                )
                popup = folium.Popup(iframe, max_width=self.POPUP_MAX_WIDTH)

                # Add a clickable marker at a specified location on the map, which displays a popup
                folium.Marker(
                    location=[int(project.latitude), int(project.longitude)],
                    tooltip="Click to view Project Summary",
                    popup=popup,
                ).add_to(self.project_map)
