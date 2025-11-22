# --------------------------------------------------------
# QTile 0.33.0 Config v.3
# --------------------------------------------------------

import os, subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, KeyChord, DropDown
from libqtile.lazy import lazy
from colors import *
from typing import List

# --------------------------------------------------------
# Definitions
# --------------------------------------------------------

mod = "mod4"
myTerm = "kitty"
myBrowser = "chromium"
myEditor = "nvim"
myFiles = "qtfm"
myCalc = "qalculate"

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'

# --------------------------------------------------------
# Key Bindings
# --------------------------------------------------------

keys = [
# Program/Functions launchers
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "r", lazy.spawn("dmenu_run -m 0"), desc="dmenu"),
    Key([mod], "b", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod, "control"], "b", lazy.spawn("qutebrowser"), desc='Web browser'),
    Key([mod], "c", lazy.spawn(myCalc), desc='Qalculate'),
    Key([mod], "f", lazy.spawn(myFiles), desc='qtfm'),
    Key([mod, "control"], "v", lazy.spawn(myTerm + " -e zathura ~/help/VimShortcuts.pdf"), desc='Vim Shortcuts'),
    Key([mod], "x", lazy.spawn("slock"), desc='Suckless Screen Locker'),
    Key([mod],	"p", lazy.spawn("maim -i $(xdotool getactivewindow) ~/Pictures/Screenshots/window-$(date '+%y%m%d-%H%M-%S').png"), desc='Screenshot Active Window'),
    Key([mod, "shift"], "p", lazy.spawn("maim ~/Pictures/Screenshots/screen-$(date '+%y%m%d-%H%M-%S').png"), desc='Screenshot Screen'),
    Key([mod, "control"], "p", lazy.spawn("ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:2 -frames 1 ~/Pictures/Screenshots/out.jpg"), desc='Camera Selfie'),
    #Key([], "XF86Launch1", lazy.spawn("zathura ~/help/KeyBindings.pdf"), desc='Key Bindings Cheatsheet'),
# Basic Operations
    Key([mod, "shift"], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    #Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "Backspace", lazy.shutdown(), desc="Quit Qtile"),
# Volume keys
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%+")),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 50%")),
    Key([mod, "control"], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 25%")),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 100%")),
    Key([mod, "control"], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 75%")),

# Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

# Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

# Grow/shrink windows left/right. This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the right"
    ),

# Grow windows up, down, left, right.  Only works in certain layouts. Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------

groups = [
        Group("1",
              label = " ",
              #label = "1",
              layout = "tile",),
        Group("2",
              label = " ",
              #label = "2",
              layout = "max",
              matches = [Match(wm_class="chromium"), Match(wm_class="qutebrowser")]),
        Group("3",
              label = " ",
              #label = "3",
              layout = "tile",
              matches = [Match(wm_class="Zathura")]),
        Group("4",
              label = " ",
              #label = "4",
              layout = "tile",
              matches = [Match(wm_class="Gimp")]),
        Group("5",
              label = " ",
              #label = "5",
              layout = "tile",
              matches = [Match(wm_class="mpv")]),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

# --------------------------------------------------------
# ScratchPads
# --------------------------------------------------------

groups.append(ScratchPad("6", [
    DropDown("terminal", "kitty", x=0.2, y=0.1, width=0.60, height=0.60, on_focus_lost_hide=False ),
    DropDown("music", "kitty -e ncmpcpp", x=0.2, y=0.1, width=0.60, height=0.60, on_focus_lost_hide=False ),
]))

keys.extend([
    Key([mod], 'F11', lazy.group["6"].dropdown_toggle("music")),
    Key([mod], 'F12', lazy.group["6"].dropdown_toggle("terminal")),
])

# --------------------------------------------------------
# Theming
# --------------------------------------------------------

colors = scheme ["Nord"]

## To set color scheme using PyWal ##
#colors = []
#cache='/home/nick/.cache/wal/colors'
# def load_colors(cache):
#    with open(cache, 'r') as file:
#        for i in range(8):
#            colors.append(file.readline().strip())
#    colors.append('#ffffff')
#    lazy.reload()
#load_colors(cache)

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layout_theme = {"border_width": 2,
                "margin": 0, #"gap" size in pixels
                "border_focus": colors[8],
                "border_normal": colors[0]
                }

layouts = [
    layout.Tile(**layout_theme, ratio=0.55),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme, ratio = 0.55),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme)
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Stack(**layout_theme, num_stacks=2),
    #layout.Columns(**layout_theme),
    #layout.Zoomy(**layout_theme),
]

# --------------------------------------------------------
# Widget Defaults
# --------------------------------------------------------

widget_defaults = dict(
    font="Source Code Pro",
    fontsize = 14,
    padding = 6,
    )

# --------------------------------------------------------
# Widget Bar
# --------------------------------------------------------

extension_defaults = widget_defaults.copy()
screens = [
	Screen(
		top = bar.Bar( [
	    widget.Spacer(
            length=10
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
        widget.Wallpaper(
            background = colors[2],
            padding = 10,
            directory = '~/Pictures/Wallpapers/',
            random_selection=True,
            foreground='1076a9',
            label=""
            ),
	    widget.Sep(
            background = colors[2],
            padding = 10,
            linewidth=2,
            foreground = '000000'),
	    widget.GroupBox(
            background = colors[2],
            margin_y = 4,
            #margin_x = 7,
            padding_y = 0,
            padding_x = 0,
            borderwidth = 3,
            active = colors[7],
            inactive = colors[9],
            rounded = False,
            highlight_color = '000000',
            highlight_method = 'line',
            hide_unused = True,
            ),
	    widget.Sep(
            background = colors[2],
            linewidth=2,
            foreground = '000000'),
        widget.CurrentLayout(
            background = colors[2],
            foreground = colors[1],
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
	    widget.Spacer(
            length=10
            ),
	    widget.Spacer(
            length=50
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
        widget.WindowName(
            background = colors[2],
            foreground = colors[6],
            max_chars = 40,
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
	    widget.Spacer(
            length=50
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
        widget.CheckUpdates(
            background = colors[2],
            colour_have_updates = colors[7],
            colour_no_updates = colors[9],
            update_interval = 28800,
            distro = 'Void',
            display_format = '  {updates}',
            no_update_string = '  0',
            ),
#        widget.Wttr(
#            update_interval = 3600,
#            foreground = colors[5],
#            location = {: 'Home'},
#            format = '%C %t',
#            units = 'u',
#            fmt = '{}',
#            ),
#        widget.CPU(
#            foreground = colors[3],
#            format = ' {load_percent}%',
#            ),
#        widget.Memory(
#            foreground = colors[5],
#            format = '{MemUsed: .0f}{mm}',
#            fmt = ' {}',
#            ),
        widget.GenPollText(
            background = colors[2],
            foreground = colors[4],
            name = 'VPN',
            update_interval = 3600,
            fmt = '{}',
            func = lambda: subprocess.check_output('/home/nick/.local/bin/network.sh').decode('utf-8').strip(),
            ),
        widget.Wlan(
            background = colors[2],
            foreground = colors[4],
            interface = 'wlp2s0',
            format = '{percent:2.0%}',
            fmt = '{}',
            ethernet_interface = 'enp0s25',
            ethernet_message_format = ' ',
            disconnected_message = ' ',
            ),
        widget.GenPollText(
            background = colors[2],
            foreground = colors[8],
            name = 'Volume',
            update_interval = 3,
            fmt = '{}',
            func = lambda: subprocess.check_output('/home/nick/.local/bin/vol.sh').decode('utf-8').strip(),
            ),
        widget.Battery(
            background = colors[2],
            foreground = colors[5],
            battery = 0,
            charge_char = '󰂄',
            full_char = '󰚥',
            full_short_text = '󰚥',
            discharge_char ='󰁾',
            empty_char = '󱊡',
            empty_short_text = '󱊡',
            low_percentage = 0.1,
            format = '{char} {percent:2.0%} {hour:d}:{min:02d}',
            fmt = '{}',
            ),
        widget.Clock(
            background = colors[2],
            foreground = colors[7],
            format = "%a %e %b %H:%M", # %a, %e %b
            ),
        widget.TextBox(
            text = '',
            foreground = colors[2],
            padding = 0,
            fontsize = 18
            ),
        widget.Spacer(
            length=10
            ),
        ], # closes widget Definitions
        20,
        background = '#00000000',
        #margin = [3, 10, 3, 10] # makes bar float with padding [N, E, S, W]
        ), # closes bar.bar
	) # closes Screen
] # closes screens

# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    # Drag(["mod1"], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    # Drag(["mod1"], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Click(["mod1"], "Button2", lazy.window.bring_to_front()),
]

# --------------------------------------------------------
# Define floating layouts
# Run the utility of `xprop` to see the wm class and name of an X client.
# --------------------------------------------------------

floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
    ]
)

# --------------------------------------------------------
# General Setup
# --------------------------------------------------------

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = "LG3D"
wmname = "QTile"
