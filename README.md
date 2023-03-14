# Appium Touch Actions

*In terms of interacting with the device, you're not limited to simple element taps. You can also construct arbitrary gestures and touch movements using the WebDriver Actions API. The stylus is the limit!*

One of the most important aspects of the mobile device user experience is the ability to use touch gestures of various kinds to control an app. Luckily, the WebDriver specification already defines a special API that allows you to define any kind of touch action, and Appium supports this API. So let's take a look at what it is and how you can use it!

Before we look at how to access this API from the client, let's first get clarity on the different terms and values involved.

| Actions API Concepts |  |
| ---- | ---- |
| Input source | The thing causing the action to happen (mouse, finger, keyboard) |
| Input source type | <code>mouse</code>, <code>pen</code> or <code>touch</code>. For Appium, always use <code>touch</code> |
| Input source action | Object that describes an action of various types: <code>pause</code>, <code>pointerDown</code>, <code>pointerUp</code>, <code>pointerMove</code> |
| Action type-specific properties | Specific info about the action. E.g., <code>duration</code>, <code>origin</code>, <code>x</code> and <code>y</code> coordinates to move to, for a <code>pointerMove</code> action. |
| Action sequence | A list of actions associated with a particular input source. |
| Multiple input sources | One "Action" may consist of multiple parallel input sources each with their own sequence. |

#### Actions API Example:

<img width="600" src="https://user-images.githubusercontent.com/70295997/223850075-8fa6d989-af26-48f2-a780-85b4fa257202.png">
<img width="600" src="https://user-images.githubusercontent.com/70295997/223855994-6e0301aa-53b6-49bf-8f3a-4fddc4e28a81.png">

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

The first action sequence starts with a <code>pointerMove</code>. This is equivalent to moving our finger somewhere above the screen before touching it down. In this case, we're going to the coordinate 100, 100. Coordinates on mobile devices are defined with 0, 0 at the top left, and increasing in each dimension towards the bottom right. So just the same as webpages. Next, we're defining a <code>pointerDown</code> action. This signifies we want to touch the finger to the screen. We have to include a <code>button</code> property here as well. This is mostly for mouse actions, but we have to include it all the same, so we just set it to 0 which refers to the left mouse button. Third, we have a <code>pause</code> action, which comes with a <code>duration</code> value of 500. The duration tells the server how long to pause in the current state, and the value is in milliseconds, so 500 milliseconds here meaning half a second. Next, we have a <code>pointerMove</code> with some additional parameters, which is the most complex of all of these actions. It has a duration as well, which says how long the move itself should take, in this case 1 second. We also have an <code>origin</code> property, which tells the server what to expect our x and y values to refer to. Origin can be either <code>pointer</code> or <code>viewport</code>, and it defaults to <code>viewport</code> as it did in our first <code>pointerMove</code> above. If we set it to pointer, then we are saying that the x and y values we include will be relative to the *current* position of the pointer. If we had set origin to <code>viewport</code>, then our x and y values would be considered as *absolute* values within the screen. So in this case, we have an x value of -50, which means 50 pixels to the left of the current position. And we have a y value of zero, which means keeping the vertical dimension the same. Our last action is a <code>pointerUp</code> action, which just means to take the finger off the screen. It's always important to do this, to clear the way for future actions!

That was all the first action sequence. What about the second? Let's focus on that object now instead. Most of this is exactly the same. We're starting the pointer at the same location, but in our second pointer move, we are instead moving our x value 50 pixels to the *right* instead of to the left. So you can visualize this touch action as involving two fingers, starting at the same place, waiting for a bit, and then moving outward horizontally to the same degree. In other words, we're performing an action that would be interpreted as a "zoom" by many apps nowadays! So this is how we might encode a zoom using the Actions API!

This is all very interesting, but it's not what we would actually write in code. This is the low-level object that would be sent by our client library to the Appium server, and I wanted you to get familiar with it so you know everything that's involved in this API, and so you know there's no magic. But now let's talk about how we might encode actions using the Python client instead.

| Python ActionBuilder API |  |
| ---- | ---- |
| <code>ActionsBuilder(driver)</code>    <code>selenium.webdriver.common.actions.action_builder</code> | Container for input sources and actions that will build ip and perform them |
| <code>action.add_pointer_input(kind, id)</code>    <code>selenium.webdriver.common.actions.interaction</code> | To add a pointer input, need to know the kind (e.g. POINTER_TOUCH) and ID (we make this up, e.g. "finger1") |

First, let's talk about the <code>ActionBuilder</code> class. This is a class we can import from <code>selenium.webdriver.common.actions.action_builder</code>, and it is the main container for working with actions. When we create an ActionBuilder object, we pass it our <code>driver</code> object, so it can go ahead and perform the actions for us when we're done. And that's exactly what we do; once we're done building actions, we call the <code>perform()</code> method on the ActionBuilder object. So how do we add actions? Well before we add actions, we first need to add the input source or sources.

To add a pointer input source, we can call the <code>add_pointer_input</code> method on the ActionBuilder object, and it will return a new pointer input for us to use. To create this object, we need two pieces of information. One is the kind of pointer input we're adding. There's a helpful constant called <code>POINTER_TOUCH</code> we can use to designate a touch pointer type, and we can import it from <code>selenium.webdriver.common.actions.interaction</code>. The other parameter is the id of this pointer, which is up to us to define. It really doesn't matter what it is, as long as it's unique. I usually call it <code>finger</code> or <code>finger1</code>. Now that we have a pointer input, we can start to build up actions on it. Let's look at the 4 actions we can use.

| Python Input Actions API |  |
| ---- | ---- |
| <code>input.create_pause(duration=1000)</code> | Creates a pause for a given number of milliseconds within the action |
| <code>input.create_pointer_down(MouseButton.LEFT)</code> | Click down (using a certain mouse button) or touch the pointer to the screen |
| <code>input.create_pointer_up(MouseButton.LEFT)</code> | Release click (given a button) or lift pointer up from screen |
| <code>input.create_pointer_move(duration, origin, x, y)</code> | Move a pointer from one place to another |

1. First, we could create a <code>pause</code> action. Again, this is an action that doesn't do anything, so we rarely need to use it. That being said, it is helpful when it comes to defining drag and drop sequences, or long presses, that kind of thing. To create a pause action we simply call <code>input.create_pause</code>, passing in a <code>duration</code> keyword argument.
2. Second, we can call <code>input.create_pointer_down</code>, which touches the pointer to the screen. This takes a single parameter, which is the ID of the mouse button to press. By convention with Appium, we always use the left mouse button for this, even though we don't have a mouse to begin with. We could use the constant 0, but that's a bit cryptic. So instead we can also import the <code>MouseButton</code> class from <code>selenium.webdriver.common.actions.mouse_button</code>, and then refer to the left mouse button as <code>MouseButton.LEFT</code>, to make it a little clearer what's happening.
3. Third, we could call <code>input.create_pointer_up</code>, which lifts the pointer up off the screen. This takes the same type of parameter as <code>create_pointer_down</code>.
4. Fourth, we could call the pointer move method using <code>input.create_pointer_move</code>. This take 4 possible keyword arguments, which we already discussed: duration, origin, x, and y. For the origin parameter, the value should either be the string "viewport", which is the default, or the string "pointer" to denote a pointer-relative move.

#### [Real-World Scenario](https://github.com/lana-20/appium-touch-actions/blob/main/gestures_android.py)
Here I've got my Android device, and I'm going to open up The App to show you what we're going to try to do using Touch Actions. On the home screen here, there's a button called List Demo. If I tap this, I get to a list view. This is a list of cloud types. Notice that not all clouds are available on the screen right now. To get to the ones at the bottom I'd have to scroll, using a sort of swiping gesture where I move my finger up the middle of the screen. This is especially crucial on Android, where these elements that are "below the fold" so to speak, are not even present in the UI hierarchy until I scroll to make them visible. So if I want to interact with these elements at all, I'll need to use a touch action to get them to show up in the first place. 

<img width="800" src="https://user-images.githubusercontent.com/70295997/223875938-66668f08-e623-447b-b853-3582e379030d.png">

<img width="300" src="https://user-images.githubusercontent.com/70295997/224865358-d813c00b-02ca-407c-83ac-4440061dfcb7.png"><img width="336" src="https://user-images.githubusercontent.com/70295997/224865295-e0fd14fd-2bb6-4b8f-bd72-17cb843cdad2.png">


Let's write an Android script with automation steps starting with the <code>wait</code>. We want to find and go to the List Demo view.

        wait.until(EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, 'List Demo'))).click()
        
That should get us to the list demo screen. I *could* start coding up my gesture right here, but I don't want to do that yet. 

This is because I want to make sure the next view is fully loaded before I go and start swiping. I don't want Appium to start the swipe while the view is in the midst of transition to the next screen. So what do I do instead? Well, what I usually do here is first encode a wait for some element that I know will exist on the next view, so that I don't start any other actions until that element has been found. For this List Demo view, I know that we have a cloud called 'Altocumulus' up top, so I'll just wait for that element:

        wait.until(EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, 'Altocumulus')))

Alright, now we're ready to start encoding our swipe action! But before I do that, I'm going to take care of some of the Python modules imports we'll need for the actions commands:

        from selenium.webdriver.common.actions.action_builder import ActionBuilder
        from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
        from selenium.webdriver.common.actions.mouse_button import MouseButton

So the first thing we want to do is create an ActionBuilder object, passing in our driver:

        actions = ActionBuilder(driver)
            finger = actions.add_pointer_input(POINTER_TOUCH, "finger")

Then, we create a pointer input that I'll call <code>finger</code>, and declare that it's a touch input. Now we can start to define our action sequence using this <code>finger</code> object. Our sequence will consist of four steps, first moving the finger to where we want our swipe to start:

        finger.create_pointer_move(duration=0, x=100, y=500)

In this case I've chosen a sort of arbitrary position of an x value of 100 and a y value of 500. In a real example, we'd want to instead get the device width and size using the Get Window Rect command, also available in Selenium, and then do some math to figure out exactly where we want our swipe to begin. Next, we move the pointer down to begin the period of time where the finger is touching the screen:

        finger.create_pointer_down(button=MouseButton.LEFT)

Now we need to move our finger while it's on the screen. To scroll the list down, we'll need to move our finger up, which we can denote by using a pointer-relative negative y-value. In this case I'll set it to -500, which is basically going to move the finger to the top of the screen. I'm also using a duration of 250 milliseconds for a relatively quick swipe.

        finger.create_pointer_move(duration=250, x=0, y=-500, origin="pointer")

And, finally, we wrap things up by taking the finger back off the screen:

        finger.create_pointer_up(button=MouseButton.LEFT)

Once all this is done, we are finished encoding our actions, and it's time to run them. Just encoding them in ActionBuilder doesn't actually run anything, and this makes sense. We don't want to run the actions one at a time, because the commands would have to go back and forth across the Internet, adding a bunch of latency to our very specific actions. Instead, we encode the actions and then send it as one big object over to the Appium server, where they are decoded and then executed just as we defined them. So to make that happen, we call the <code>perform()</code> method on our ActionBuilder object:

        actions.perform()

So that should scroll us down. To prove that it actually worked, I'm going to try and find an element that I should only be able to find if I've scrolled near the bottom of the list. There's a cloud that starts with S, Stratocumulus, that should do the trick. So I'll just put a basic Find Element command here to make that happen:

        driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Stratocumulus')

Run the script to prove that the Actions-based swipe worked.

This is basically everything there is to the Actions API. But it's by no means the most complex thing you can do with it. The Actions API is a totally general approach to defining touch actions, so it can get quite interesting. You can define quite complex gestures that follow particular shapes or patterns, and even use multiple input sources at once, if your app supports it.

















