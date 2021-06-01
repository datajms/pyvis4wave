from h2o_wave import main, app, Q, ui, listen

# Import graph
from .network import WaveNetwork
from .wave_events import UiVis4Wave

main


def build_demo_network():
    """
    Define your graph in this function
    You can use the syntax of the pyvis library
    Code: https://github.com/WestHealth/pyvis
    Docs: https://pyvis.readthedocs.io/en/latest/tutorial.html

    :return: a WaveNetwork object
    """
    g = WaveNetwork(height="600px", width="600px")  # It has the same syntax as in pyvis
    g.add_node(0, label="id: 0")
    g.add_node(1, label="id: 1")
    g.add_edge(0, 1, label="from 0 to 1")

    return g


@app("/demo")
async def serve(q: Q):
    if not q.client.initialized:
        q.page["meta"] = ui.meta_card(box="")

        g = build_demo_network()

        ui_vis4wave = UiVis4Wave(q, g, wave_name="myynetwork")
        q.user.event_catcher = ui_vis4wave.get_event_catcher()

        q.page["myvis"] = ui_vis4wave.get_card(
            box="1 1 6 8",
            title="Try to click, double-click, hover, add or delete edges and nodes",
        )

        q.page["details"] = ui.markdown_card(
            box="1 9 6 2",
            title="",
            content="Default value ",
        )

        # Build network:

        q.client.initialized = True

    output_value = q.user.event_catcher.catch(q)
    if len(output_value) > 0:
        q.page["details"].content = "\n".join([str(dic) for dic in output_value])

    await q.page.save()


if __name__ == "__main__":
    print("-----------------------------------")
    print("Welcome to the pyvis4wave demo App!")
    print(" Go to http://localhost:10101/demo ")
    print("-----------------------------------")
    listen("/", serve)
