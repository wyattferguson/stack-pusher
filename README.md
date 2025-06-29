![StackPusher](https://i.imgur.com/kKjIvCo.gif)

# :joystick: Stack Pusher

A remake of the classic flash game ores with Pyxels. This project is basically a rough demo, that I would like to port to the Gameboy in the near future.

Stop the blocks from being pushed of the screen! Destroy touching blocks of the same color to earn points towards leveling up. When you level up the screen restarts, but gets tougher every level. If the blocks go off the left side of the screen you lose.

### :rocket: [Play in your browser]([https://wyattferguson.github.io/](https://wyattferguson.github.io/stackpusher.html))

## Controls

```
W,A,S,D - Movement
F - Push stack forward
Space - Select a block
R - Restart Game
P - Pause Game
```

## Development Setup

Installation is pretty straight forward, Im using [UV](https://docs.astral.sh/uv/) to manage everything.

To get it all running from scratch:

```
# spin up a virtual enviroment
uv venv

# activate virtual enviroment
.venv\Scripts\activate

# install all the cool dependancies
uv sync

# run game
task run

# build html version
task build

# lint source
task lint

# format source with ruff
task format
```

## References

- Pyxel ([https://github.com/kitao/pyxel](https://github.com/kitao/pyxel))
- Orignal Ores Gameplay ([https://www.youtube.com/watch?v=vVu9ROoBZKQ](https://www.youtube.com/watch?v=vVu9ROoBZKQ))

## Contact & Support

Created by [Wyatt Ferguson](https://github.com/wyattferguson)

For any questions or comments heres how you can reach me:

### :octocat: Follow me on [Github @wyattferguson](https://github.com/wyattferguson)

### :mailbox_with_mail: Email me at [wyattxdev@duck.com](wyattxdev@duck.com)

### :shaved_ice: Follow on [BlueSky @wyattf](https://wyattf.bsky.social)

If you find this useful and want to tip me a little coffee money:

### :coffee: [Buy Me A Coffee](https://www.buymeacoffee.com/wyattferguson)
