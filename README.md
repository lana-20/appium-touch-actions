# Appium Touch Actions

One of the most important aspects of the mobile device user experience is the ability to use touch gestures of various kinds to control an app. Luckily, the WebDriver specification already defines a special API that allows you to define any kind of touch action, and Appium supports this API. So let's take a look at what it is and how you can use it!

Before we look at how to access this API from the client, let's first get clarity on the different terms and values involved.

| Actions API Concepts |  |
| ---- | ---- |
| Input source | The thing causing the action to happen (mouse, finger, keyboard) |
| Input source type | <code>mouse</code>, <code>pen</code> or <code>touch</code>. For Appium, always use <code>touch</code> |
| Input source action | Object that describes an action of various types: <code>pause</code>, <code>pointerDown</code>, <code>pointerUp</code>, <code>pointerMove</code> |
| Action type-specific properties | Specific info about the action. E.g., <code>duration</code>, <code>x</code>, or <code>y</code> for a <code>pointerMove</code> action. |
| Action sequence | A list of actions associated with a particular input source. |
| Multiple input sources | One "Action" may consist of multiple parallel input sources each with their own sequence. |


1. First, we have the concept of an 'input source'. An input source is just another name for the thing that is causing the action to happen. The actions API actually has support for more than touch gestures. It also has support for holding down keys on a keyboard. So there are really two kinds of input source. One kind is called 'pointer', which refers to either a mouse pointer or a finger pointer. Anything that can move and click or tap. The other kind of input source is called 'key'. We're going to focus on pointer input sources, since that's what we use for touch actions.
2. If we have a pointer input source, then in addition we can also specify the type of the input source. This can be either <code>mouse</code>, <code>pen</code>, or <code>touch</code>. For website automation, we would probably use a mouse pointer type. But for Appium scripts running on mobile devices, we'll need to use the <code>touch</code> input type.
3. Once we have an input source defined, we can start to associate "actions" with it. Each action is itself an object which has various properties depending on the kind of input source it's associated with. For pointer input sources, we have a <code>type</code> key, which can be one of the following types: <code>pause</code>, which is an action that just sits and does nothing. <code>pointerDown</code>, which moves the pointer down to touch the screen. <code>pointerUp</code>, which does the opposite and moves the pointer off the screen. And finally, <code>pointerMove</code>, which moves the pointer to a new location.
4. Depending on the type of action we're dealing with, there would be additional properties. For example, the <code>pause</code> action type requires that you also include a <code>duration</code> property. Or as you can imagine, the <code>pointerMove</code> action requires that you include information about the <code>x</code> and <code>y</code> location you want the pointer to move to.
5. For each input source, we can actually define a whole sequence of actions, not just one. These will be executed one right after the other.
6. And finally, we're not limited to just one input source. We can actually define multiple input sources, reflecting the reality that we can use multiple fingers to interact with our device. The actions defined by each of these input sources will be executed side-by-side, so it's up to us to figure out which actions need to take place at the same time if we're using different input sources.

Let's look at an example of how we might encode a certain action using JSON. JSON is ultimately what gets sent to the Appium server, so this is entirely appropriate, even though it's not super helpful or convenient to look at.

    [
      {
        "type": "pointer",
        "id": "finger1",
        "parameters": {"pointerType": "touch"},
        "actions": [
          {"type": "pointerMove", "duration": 0, "x": 100, "y": 100},
          {"type": "pointerDown", "button": 0},
          {"type": "pause", "duration": 500},
          {"type": "pointerMove", "duration": 1000, "origin": "pointer", "x": -50, "y": 0},
          {"type": "pointerUp", "button": 0}
        ]
      }, {
        "type": "pointer",
        "id": "finger2",
        "parameters": {"pointerType": "touch"},
        "actions": [
          {"type": "pointerMove", "duration": 0, "x": 100, "y": 100},
          {"type": "pointerDown", "button": 0},
          {"type": "pause", "duration": 500},
          {"type": "pointerMove", "duration": 1000, "origin": "pointer", "x": 50, "y": 0},
          {"type": "pointerUp", "button": 0}
        ]
      }
    ]

So, what's going on here? Let's break it down. What we have is a list of objects. There are two objects at the main level in this list. It's quite small so let's zoom in on just the first object.

The first one declares that it has a type of <code>pointer</code>, so it is an input source object defining a pointer input. We've given it an id of <code>finger</code>, and said that it has a <code>pointerType</code> of <code>touch</code>. OK, so now we can see that this object is defining actions for a finger! But we have another one defined below, which we've called <code>finger2</code>. So it looks like what's going on is that we have a 2-finger gesture. But what gesture is it? Let's take a look at the <code>actions</code> list inside each input source. In each action list we have 5 actions defined, which is good, because we always want the number of actions to match across input sources.

The first action sequence starts with a pointerMove. This is equivalent to moving our finger somewhere above the screen before touching it down. In this case, we're going to the coordinate 100, 100. Coordinates on mobile devices are defined with 0, 0 at the top left, and increasing in each dimension towards the bottom right. So just the same as webpages. Next, we're defining a pointerDown action. This signifies we want to touch the finger to the screen. We have to include a button property here as well. This is mostly for mouse actions, but we have to include it all the same, so we just set it to 0 which refers to the left mouse button. Third, we have a pause action, which comes with a duration value of 500. The duration tells the server how long to pause in the current state, and the value is in milliseconds, so 500 milliseconds here meaning half a second. Next, we have a pointerMove with some additional parameters, which is the most complex of all of these actions. It has a duration as well, which says how long the move itself should take, in this case 1 second. We also have an origin property, which tells the server what to expect our x and y values to refer to. Origin can be either pointer or viewport, and it defaults to viewport as it did in our first pointerMove above. If we set it to pointer, then we are saying that the x and y values we include will be relative to the current position of the pointer. If we had set origin to viewport, then our x and y values would be considered as absolute values within the screen. So in this case, we have an x value of -50, which means 50 pixels to the left of the current position. And we have a y value of zero, which means keeping the vertical dimension the same. Our last action is a pointerUp action, which just means to take the finger off the screen. It's always important to do this, to clear the way for future actions!

OK, that was all the first action sequence. What about the second? Let's focus on that object now instead. Most of this is exactly the same. We're starting the pointer at the same location, but in our second pointer move, we are instead moving our x value 50 pixels to the right instead of to the left. So you can visualize this touch action as involving two fingers, starting at the same place, waiting for a bit, and then moving outward horizontally to the same degree. In other words, we're performing an action that would be interpreted as a "zoom" by many apps nowadays! So this is how we might encode a zoom using the Actions API!

OK this is all very interesting, but it's not what we would actually write in code. This is the low-level object that would be sent by our client library to the Appium server, and I wanted you to get familiar with it so you know everything that's involved in this API, and so you know there's no magic. But now let's talk about how we might encode actions using the Python client instead.

First, let's talk about the ActionBuilder class. This is a class we can import from selenium.webdriver.common.actions.action_builder, and it is the main container for working with actions. When we create an ActionBuilder object, we pass it our driver object, so it can go ahead and perform the actions for us when we're done. And that's exactly what we do; once we're done building actions, we call the perform() method on the ActionBuilder object! So how do we add actions? Well before we add actions, we first need to add the input source or sources.

To add a pointer input source, we can call the add_pointer_input method on the ActionBuilder object, and it will return a new pointer input for us to use. To create this object, we need two pieces of information. One is the kind of pointer input we're adding. There's a helpful constant called POINTER_TOUCH we can use to designate a touch pointer type, and we can import it from selenium.webdriver.common.actions.interaction. The other parameter is the id of this pointer, which is up to us to define. It really doesn't matter what it is, as long as it's unique. I usually call it finger or finger1. OK, now that we have a pointer input, we can start to build up actions on it. Let's look at the 4 actions we can use.

First, we could create a pause action. Again, this is an action that doesn't do anything, so we rarely need to use it. That being said, it is helpful when it comes to defining drag and drop sequences, or long presses, that kind of thing. To create a pause action we simply call input.create_pause, passing in a duration keyword argument.
Second, we can call input.create_pointer_down, which touches the pointer to the screen. This takes a single parameter, which is the ID of the mouse button to press. By convention with Appium, we always use the left mouse button for this, even though we don't have a mouse to begin with. We could use the constant 0, but that's a bit cryptic. So instead we can also import the MouseButton class from selenium.webdriver.common.actions.mouse_button, and then refer to the left mouse button as MouseButton.LEFT, to make it a little clearer what's happening.
Third, we could call input.create_pointer_up, which lifts the pointer up off the screen. This takes the same type of parameter as create_pointer_down.
Fourth, we could call the pointer move method using input.create_pointer_move. This take 4 possible keyword arguments, which we already discussed: duration, origin, x, and y. For the origin parameter, the value should either be the string "viewport", which is the default, or the string "pointer" to denote a pointer-relative move.
