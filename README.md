# Pyvis component for H2O wave
Bringing interactive network visualization to H2O wave web-apps


## Quick Start

In your H2O wave app, add a pyvis4wave component to:
- display a network and edit it (thanks to pyvis and visjs)
- catch the user actions (node/edge clicked, hovered; node/edge added, deleted)


In your wave app:
1. Define your network
    ```python
    # Define the WaveNetwork component
    from vis4wave.network import WaveNetwork

    g = WaveNetwork()  # It has the same syntax as in pyvis
    g.add_node(0)
    g.add_node(1)
    g.add_edge(0, 1)
    ```
2. Display the network
    ```python
    # Display your WaveNetwork component
    from vis4wave.wave_events import UiVis4Wave

    ui_vis4wave = UiVis4Wave(
        q,  # The Q object from wave
        wave_network_object=g,  # A object of class WaveNetwork
        wave_name="myynetwork"  # An id name for the object (the html div name)
    )

    # Initialize your pyvis4wave event_catcher (see below)
    q.user.event_catcher = ui_vis4wave.get_event_catcher()

    # Define your wave UI card
    q.page["myvis"] = ui_vis4wave.get_card(
        box="1 1 6 8",
        title="Try to click, double-click, hover, add or delete edges and nodes",
    )
    ```
3. Catch the user interactions / events (click on node, on edge, hover, delete, etc.)
    ```python
    # This should be in the main 'serve(q)' function of the wave app.

    # Use the event_catcher which targets your network object
    output_value = q.user.event_catcher.catch(q)

    if len(output_value) == 0:
        pass  # Nothing to catch, no user interaction
    else:
        for event_catched in output_value:
            # event_catched is a dict which one single key: the event type
            print(f"Type of event catched: {event_catched.keys()[0]}")
            print(f"Details of event: {event_catched.values()[0]}")  # The details depends
            # on the type of event.
            # It could be a node id, an edge id, an edge definition (from X to X), etc.
    ```

## Demo

You can also run the demo locally:
1. Run a wave server (≥ 0.16). See [wave docs](https://wave.h2o.ai/docs/installation) for installation,
go through step 1 to 5 of these docs.
2. Install this package (instructions coming soon) and run:
```wave run vis4wave/demo_wave_network.py```
3. Go to your browser: ```http://localhost:10101/demo```
