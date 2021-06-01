from h2o_wave import Q, ui


class UiVis4Wave:
    def __init__(self, q: Q, wave_network_object, wave_name="mynetwork"):
        self.wave_name = wave_name
        self.div_html = None

        # Activate the Edit menu (add node, add edge, delete, etc.)
        wave_network_object.set_manipulation_option(True)

        # Allow to send hover callbacks (deactivate if the flooding of events makes things slow)
        wave_network_object.set_hover_callbacks_option(True)

        # Use return_html to render object that will be ingested
        div_html, js_script = wave_network_object.return_html(wave_name=self.wave_name)

        self.div_html = div_html

        # Update scripts within wave object
        q.page["meta"].scripts = [
            ui.script(
                path="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"
            )
        ]
        # Call Javascript to render our graph using vis.js.
        q.page["meta"].script = ui.inline_script(
            content=js_script, requires=["vis"], targets=[wave_name]
        )

    def get_event_catcher(self, *args, **kwargs):
        # Init event catcher
        # You can change the defaults to only catch the events type that you want
        event_catcher = VisEventCatcher(wave_name=self.wave_name, *args, **kwargs)

        return event_catcher

    def get_card(self, box, title=""):
        card = ui.markup_card(box=box, title=title, content=self.div_html)
        return card


class VisEventCatcher:
    def __init__(
        self,
        wave_name,
        click=True,
        double_click=True,
        hover=True,
        add=True,
        edit=True,
        delete=True,
        zoom=False,
    ):
        """
        :param wave_name, str. The name of the html div which hosts the network. It should be the same string as in vis4wave.WaveNetwork.return_html(wave_name)
        :param click: bool, whether `click` events should trigger the catch method
        :param double_click: bool, whether `double_click` events should trigger the catch method
        :param hover: bool, whether `hover` events should trigger the catch method
        :param zoom: bool, whether `zoom` events should trigger the catch method
        :param add: bool, whether `add` events should trigger the catch method
        :param edit: bool, whether `edit` events should trigger the catch method
        :param delete: bool, whether `delete` events should trigger the catch method
        """
        if wave_name is None or type(wave_name) != str:
            raise ValueError(
                """wave_name should be a str: the name of the html div which hosts the network.
It should be the same string as in vis4wave.WaveNetwork.return_html(wave_name)"""
            )
        self.wave_name = wave_name

        self.click = click
        self.double_click = double_click
        self.hover = hover
        self.add = add
        self.edit = edit
        self.delete = delete
        self.zoom = zoom

    def catch(self, q):
        """
        inspect the content of q.events to see if it contains some events that need to be catched

        :param q: the wave main object
        :return: a list of dict. Empty list if no event was catched. If
        """
        output_value = []

        if q.events[self.wave_name]:
            if q.events[self.wave_name].params:

                incoming_event_params = q.events[self.wave_name].params

                if incoming_event_params["event"] in ["add__node", "add__edge"]:
                    if self.add and incoming_event_params["event"] == "add__node":
                        output_value = [
                            {"add__node": incoming_event_params["data"]["id"]}
                        ]
                    if self.add and incoming_event_params["event"] == "add__edge":
                        output_value = [{"add__edge": incoming_event_params["data"]}]

                elif incoming_event_params["event"] in ["delete__node", "delete__edge"]:
                    if self.delete and incoming_event_params["event"] == "delete__node":
                        # Send instruction to delete edges
                        for edge_deleted in incoming_event_params["data"]["edges"]:
                            output_value.append({"delete__edge": edge_deleted})
                        # Delete node
                        for node_deleted in incoming_event_params["data"]["nodes"]:
                            output_value.append({"delete__node": node_deleted})
                    if self.delete and incoming_event_params["event"] == "delete__edge":
                        for edge_deleted in incoming_event_params["data"]["edges"]:
                            output_value.append({"delete__edge": edge_deleted})

                elif incoming_event_params["event"] in ["edit__edge", "edit__node"]:
                    if self.edit and incoming_event_params["event"] == "edit__node":
                        output_value = [{"edit__node": incoming_event_params["data"]}]
                    if self.edit and incoming_event_params["event"] == "edit__edge":
                        output_value = [{"edit__edge": incoming_event_params["data"]}]

                elif incoming_event_params["event"] in ["click__edge", "click__node"]:
                    if self.click and incoming_event_params["event"] == "click__node":
                        for node_clicked in incoming_event_params["nodes"]:
                            output_value.append({"click__node": node_clicked})
                    if self.click and incoming_event_params["event"] == "click__edge":
                        for edge_clicked in incoming_event_params["edges"]:
                            output_value.append({"click__edge": edge_clicked})

                elif incoming_event_params["event"] in [
                    "double_click__edge",
                    "double_click__node",
                ]:
                    if self.double_click:
                        if incoming_event_params["event"] == "double_click__node":
                            for node_clicked in incoming_event_params["nodes"]:
                                output_value.append(
                                    {"double_click__node": node_clicked}
                                )
                        if incoming_event_params["event"] == "double_click__edge":
                            for edge_clicked in incoming_event_params["edges"]:
                                output_value.append(
                                    {"double_click__edge": edge_clicked}
                                )

                elif incoming_event_params["event"] in ["zoom__in", "zoom__out"]:
                    if self.zoom:
                        output_value = [{"zoom": incoming_event_params["event"]}]

                elif incoming_event_params["event"] in ["hover__edge", "hover__node"]:
                    if self.hover and incoming_event_params["event"] == "hover__node":
                        output_value.append(
                            {"hover__node": incoming_event_params["node"]}
                        )
                    if self.hover and incoming_event_params["event"] == "hover__edge":
                        output_value.append(
                            {"hover__edge": incoming_event_params["edge"]}
                        )

        return output_value
