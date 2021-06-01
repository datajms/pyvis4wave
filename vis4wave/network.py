from pyvis.network import Network
from jinja2 import Template


class Object(object):
    pass


class WaveNetwork(Network):
    def __init__(self, *args, **kwargs):
        """
        This class inherits all parameters from Network class from pyvis.network
        See documentation: https://github.com/WestHealth/pyvis/blob/master/pyvis/network.py
        """
        Network.__init__(self, *args, **kwargs)

    def set_manipulation_option(self, status=False):
        """

        :param status:
        :return:
        """

        if "manipulation" not in self.options.__dict__:
            self.options.manipulation = Object()
        setattr(self.options.manipulation, "enabled", status)
        return self

    def set_hover_callbacks_option(self, status=False):
        if "interaction" not in self.options.__dict__:
            self.options.interaction = Object()
        setattr(self.options.interaction, "hover", status)
        if "interaction" not in self.options.__dict__:
            self.options.interaction = Object()
        setattr(self.options.interaction, "hover_callback", status)

        return self

    def return_html(self, wave_name="mynetwork"):
        """
        This method gets the data structures supporting the nodes, edges,
        and options and updates the template to write the HTML holding
        the visualization.
        It is heavily inspired from the write_html method of Network class from pyvis.network
        The differences are:
            - it returns two objects that can be injected in wave framework: a js script and
            the div (+ its style) html object
            - there is not

        """

        # here, check if an href is present in the hover data
        use_link_template = False
        for n in self.nodes:
            title = n.get("title", None)
            if title:
                if "href" in title:
                    """
                    this tells the template to override default hover
                    mechanic, as the tooltip would move with the mouse
                    cursor which made interacting with hover data useless.
                    """
                    use_link_template = True
                    break

        js_template_path = "vis4wave/templates/js_template.js"
        div_template_path = "vis4wave/templates/div_html_template.html"

        nodes, edges, heading, height, width, options = self.get_network_data()

        # check if physics is enabled
        if isinstance(self.options, dict):
            if "physics" in self.options and "enabled" in self.options["physics"]:
                physics_enabled = self.options["physics"]["enabled"]
            else:
                physics_enabled = True
        else:
            physics_enabled = self.options.physics.enabled

        # js_script
        with open(js_template_path) as f:
            content = f.read()
        js_template = Template(content)
        js_script = js_template.render(
            height=height,
            width=width,
            nodes=nodes,
            edges=edges,
            heading=heading,
            options=options,
            physics_enabled=physics_enabled,
            use_DOT=self.use_DOT,
            dot_lang=self.dot_lang,
            widget=self.widget,
            bgcolor=self.bgcolor,
            conf=self.conf,
            tooltip_link=use_link_template,
            wave_name=wave_name,
        )

        # html div + style
        with open(div_template_path) as f:
            content = f.read()
        div_template = Template(content)
        div_html = div_template.render(
            height=height,
            width=width,
            nodes=nodes,
            edges=edges,
            heading=heading,
            options=options,
            physics_enabled=physics_enabled,
            use_DOT=self.use_DOT,
            dot_lang=self.dot_lang,
            widget=self.widget,
            bgcolor=self.bgcolor,
            conf=self.conf,
            tooltip_link=use_link_template,
            wave_name=wave_name,
        )
        return div_html, js_script
