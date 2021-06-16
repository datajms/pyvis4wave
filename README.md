# Pyvis component for H2O wave
Bringing interactive network visualization to H2O wave web-apps


## What will pyvis4wave do for me?

pyvis4wave allows you, python data-scientist/developer, to take the best out of [H2O wave](https://wave.h2o.ai/) (a python webapp framework) interactivity, to **let the user interact with graph/network visualization**.
It handles for you the bit of javascript and html configuration required to make it work, so that **you can focus what you do best**, getting interactive things working without handling html and js.
With a few lines of pure python (see [Quick Start](#quick-start) below), you can:
- Define your graph object (a [pyvis](https://github.com/WestHealth/pyvis) object with pyvis syntax), where a [lot of customization](https://pyvis.readthedocs.io/en/latest/tutorial.html#visualization) is possible
- Initialize your UiVis4Wave object to get a *back-end* event_catcher and a *front-end* ui wave card.
- Insert the event_catcher in your app, to catch the user-interactions.

Here is how the [demo](#demo) renders:
![Demo of pyvis4wave](static/demo_pyvis4wave.gif)

Currently, supported user interactions are (see event_catcher [code](https://github.com/datajms/pyvis4wave/blob/main/vis4wave/wave_events.py#L80-L158)):
- hovering of a node or an edge: returns id of object
- click on a node or an edge: returns id of object
- double click on a node or an edge: returns id of object
- user adds a new node: creates and returns the new id
- user adds a new edge: creates and returns the new id, + its 2 nodes id
- user deletes a node or an edge: returns id of delete objects
- zoom in or zoom out


## Install
It is available from PyPI
```
pip install pyvis4wave
```

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

You can also run the demo locally (`demo_wave_network.py` in the `pyvis4wave` folder`):
1. Run a wave server (≥ 0.16). See [wave docs](https://wave.h2o.ai/docs/installation) for installation,
go through step 1 to 5 of these docs.
2. Install this package (instructions coming soon) and run:
```wave run vis4wave/demo_wave_network.py```
3. Go to your browser: ```http://localhost:10101/demo```


## Contribute

Help wanted on these items:
- Make the Edit menu more beautiful: currently the Edit menu (top-left of the plot) is not as beautiful as in the pure visjs library (see it [here](https://visjs.github.io/vis-network/examples/network/other/manipulationEditEdgeNoDrag.html)).
What it is needed is to deepdive in html and css code and make changes accordingly.
