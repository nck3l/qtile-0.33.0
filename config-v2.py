# --------------------------------------------------------
# QTile 0.34.0 Config v.2
# --------------------------------------------------------

import os, subprocess, colors
from libqtile import bar, extension, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, KeyChord, DropDown
from libqtile.lazy import lazy
from typing import List
from pathlib import Path
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

# --------------------------------------------------------
# Definitions
# --------------------------------------------------------

mod = "mod4"
myTerm = "alacritty"
#myTerm = "st"
# myBrowser = "firefox"
myBrowser = "chromium"
myEditor = "nvim"
myCalc = "qalculate-qt"
launcher = "rofi -show drun"
#launcher = "dmenu_run -m 0"
home = str(Path.home())

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

#Functions to Increase/Decrease/Reset Gap sizes
@lazy.layout.function
def increase_gaps(self):
    self.margin += 5
    self.group.layout_all()

@lazy.layout.function
def decrease_gaps(self):
    new_margin = self.margin - 5
    if new_margin < 0:
        new_margin = 0
    self.margin = new_margin
    self.group.layout_all()

@lazy.layout.function
def reset_gaps(self):
    self.margin = 0
    self.group.layout_all()

# --------------------------------------------------------
# Theming
# --------------------------------------------------------

#colors = colors.Nord
colors = colors.MonokaiPro
#colors = colors.OceanicNext
#colors = colors.Palenight
#colors = colors.SolarizedDark
#colors = colors.TomorrowNight
#colors = colors.GruvboxDark
#colors = colors.DoomOne
#colors = colors.Dracula
#colors = colors.SolarizedLight

# --------------------------------------------------------
# Key Bindings
# --------------------------------------------------------

keys = [
# Program/Functions launchers
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "r", lazy.spawn(launcher), desc="Program Launcher"),
    Key([mod], "w", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod], "c", lazy.spawn(myCalc), desc='Qalculate'),
    Key([mod, "control"], "v", lazy.spawn("zathura ~/help/VimShortcuts.pdf"), desc='Vim Shortcuts'),
    Key([], "F2", lazy.spawn("physlock -p 'What are you doing here?'"), desc='physlock Screen Locker'),
    Key([], "F7", lazy.spawn("feh --bg-fill -z ~/Pictures/Wallpapers/", shell=True), desc='Change Wallpaper'),
    Key([], "F3", lazy.spawn("bash " + home + "/.local/scripts/configs.sh"), desc="Config editing script"),
    Key([], "F4", lazy.spawn("bash " + home + "/.local/scripts/latex-creator.sh"), desc="Latex Document Creator"),
    Key([], "Print", lazy.spawn(home + "/.local/bin/screenshot"), desc='Screenshot'),
    Key([], "F6", lazy.spawn(home + "/.local/bin/record"), desc="Luke Smith's screencasting dmenu script"),
    Key([mod], "F6", lazy.spawn(home + "/.local/bin/record" + "kill"), desc="Stop recording"),
#    Key([], "F8", lazy.spawn(home + "/.local/bin/mounter"), desc="Luke Smith's disk mounter"),
#    Key([mod], "F8", lazy.spawn(home + "/.local/bin/unmounter"), desc="Luke Smith's disk mounter"),
    #Key([mod, "control"], "p", lazy.spawn("ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:2 -frames 1 /home/nick/Pictures/Screenshots/out.jpg"), desc='Camera Selfie'),
# Basic Operations
    Key([mod, "shift"], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "Backspace", lazy.shutdown(), desc="Quit Qtile"),
# Volume keys
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%+")),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 50%")),
    Key([mod, "mod1"], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 25%")),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 100%")),
    Key([mod, "mod1"], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 75%")),
# Changing Focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "k", lazy.window.move_to_top(), desc="Move Window to Master"), # Doesn't work with Monad(T/W)
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod, "shift"], "j", lazy.window.move_to_bottom(), desc="Move Window to bottom of stack"), # Doesn't work with Monad(T/W)
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),
    Key([mod, "mod1"], "space", lazy.layout.shuffle_up(), desc="Move window up the stack"),
    Key([mod, "control"], "space", lazy.layout.shuffle_down(), desc="Move window down the stack"),
# Toggle split. Split = all windows displayed
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
# Grow/shrink windows left/right for MonadTall, MonadWide, bsp, and Columns layouts.
    Key([mod, "mod1"], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide", "tile"]),
        desc="Grow window to the left"
    ),
    Key([mod, "mod1"], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide", "tile"]),
        desc="Grow window to the right"
    ),
# Increase/Decrease/Reset Gaps
    Key([mod], "g", increase_gaps(), desc="Increase Gaps"),
    Key([mod, "shift"], "g", decrease_gaps(), desc="Decrease Gaps"),
    Key([mod, "mod1"], "g", reset_gaps(), desc="Reset Gaps"),
# Grow windows up, down, left, right for bsp and Columns.
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
              label = "",
              #label = "󰽧",
              layout = "tile",),
        Group("2",
              label = "",
              #label = "",
              #label = "󰽡",
              layout = "max", matches = [Match(wm_class="librewolf"), Match(wm_class="chromium"), Match(wm_class="firefox")]),
        Group("3",
              label = "",
              #label = "󰽨",
              layout = "tile", matches = [Match(wm_class="Zathura")]),
        Group("4",
              label = "",
              #label = "󰽢",
              layout = "floating", matches = [Match(wm_class="Gimp")]),
        Group("5",
              label = "󰣙",
              #label = "",
              #label = "󰽦",
              layout = "tile"),
#        Group("6",
#              label = "󱃎",
#              #label = "󰽣",
#              layout = "tile"),
#        Group("7",
#              label = "󰍘",
#              #label = "󰽥",
#              layout = "tile"),
#        Group("8",
#              label = "",
#              #label = "󰽤",
#              layout = "tile"),
]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
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

groups.append(ScratchPad("9", [
    DropDown("terminal", myTerm, x=0.2, y=0.1, width=0.60, height=0.60, on_focus_lost_hide=False ),
    DropDown("music", myTerm + " -e ncmpcpp", x=0.2, y=0.1, width=0.60, height=0.60, on_focus_lost_hide=False ),
    DropDown("lf", myTerm + " -e lf", x=0.2, y=0.1, width=0.60, height=0.60, on_focus_lost_hide=False ),
]))

keys.extend([
    Key([], 'F9', lazy.group["9"].dropdown_toggle("terminal")),
    Key([], 'F10', lazy.group["9"].dropdown_toggle("music")),
    Key([], 'F11', lazy.group["9"].dropdown_toggle("lf")),
])

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layout_theme = {"border_width": 2,
                "margin": 0, #"gap" size in pixels
                "border_focus": colors[6],
                "border_normal": colors[0]
                }

layouts = [
    layout.Tile(**layout_theme, ratio=0.55),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme)
    #layout.MonadTall(**layout_theme, ratio = 0.55, new_client_position='top'),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Stack(**layout_theme, num_stacks=2),
    #layout.Columns(**layout_theme),
    #layout.Zoomy(**layout_theme),
]

# --------------------------------------------------------
# Decorations
# https://qtile-extras.readthedocs.io/en/stable/manual/how_to/decorations.html
# --------------------------------------------------------

decor_left = {
    "decorations": [
        PowerLineDecoration(
            # path="arrow_left"
            # path="rounded_left"
            path="forward_slash"
            # path="back_slash"
        )
    ],
}

decor_right = {
    "decorations": [
        PowerLineDecoration(
            # path="arrow_right"
            # path="rounded_right"
            # path="forward_slash"
            path="back_slash"
        )
    ],
}
# --------------------------------------------------------
# Widget Defaults
# --------------------------------------------------------

widget_defaults = dict(
    font="Hack Nerd Font Propo",
    fontsize = 14,
    padding = 4,
    )

# --------------------------------------------------------
# Widget Bar
# --------------------------------------------------------

extension_defaults = widget_defaults.copy()
screens = [
	Screen(
		top = bar.Bar( [
# Left Widget area
	    widget.Spacer(
           **decor_right,
           length=10
           ),
	    widget.GroupBox(
            **decor_left,
            background = colors[2],
            margin_y = 4,
#            margin_x = 6,
            padding_y = 0,
            padding_x = 1,
            borderwidth = 3,
            active = '#478061',
            inactive = colors[9],
            rounded = False,
#            this_screen_border = colors[1],
#            this_current_screen_border = '#3E363F',
            this_current_screen_border = '#000000',
            highlight_method = 'block',
            hide_unused = False,
            ),
# Middle Widget area
	    widget.Spacer(
            **decor_right,
            length=50
            ),
        widget.WindowName(
            **decor_left,
            background = colors[2],
            foreground = colors[6],
            max_chars = 60,
            ),
# Right Widget area
	    widget.Spacer(
            **decor_right,
            length=50
            ),
        widget.CheckUpdates(
            background = colors[2],
            colour_have_updates = "#478061",
            colour_no_updates = colors[9],
            update_interval = 3600,
            distro = 'Void',
            display_format = ' {updates}',
            no_update_string = '󰜺',
            ),
#        widget.Wttr(
#            update_interval = 3600,
#            foreground = colors[5],
#            location = {: 'Home'},
#            format = '%C %t',
#            units = 'u',
#            fmt = '{}',
#            ),
        widget.CPU(
            background = colors[2],
            foreground = colors[7],
            format = ' {load_percent:.0f}%',
            ),
        widget.Memory(
            background = colors[2],
            foreground = colors[5],
            format = '{MemUsed:.0f}{mm}',
            fmt = ' {}',
            ),
        widget.GenPollText(
            background = colors[2],
            foreground = colors[8],
            name = 'NETWORK',
            update_interval = 10,
            fmt = '{}',
            func = lambda: subprocess.check_output(home + '/.local/scripts/network.sh').decode('utf-8').strip(),
            ),
        widget.GenPollText(
            background = colors[2],
            foreground = colors[6],
            name = 'Volume',
            update_interval = 2,
            fmt = '{}',
            func = lambda: subprocess.check_output(home + '/.local/scripts/vol.sh').decode('utf-8').strip(),
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
            notify_below = 0.2,
            format = '{char} {percent:2.0%} {hour:d}:{min:02d}',
            fmt = '{}',
            ),
 #       widget.Bluetooth(
 #           background = colors[2],
 #           foreground = '#1c39bb',
 #           default_show_battery = true,
 #           symbol_connected = '󰂱',
 #           symbol_paired = '',
 #           symbol_discovery = ('󰂳',''),
 #           symbol_powered = ('󰥉','󰤾'),
 #           adapter_format = '{symbol}{name} [{powered}{discovery}]'),
        widget.Clock(
            **decor_left,
            background = colors[2],
            foreground = colors[3],
            format = "%e %b %H:%M", # %a, %e %b
            ),
        widget.Spacer(
            length=10
            ),
        ], # closes widget Definitions
        20,
        background = '#00000000', # makes the bar black with complete transparency
         margin = [3, 0, 3, 0] # makes bar float with padding [N, E, S, W]
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

# Only java UI toolkits are concerned with this seting; see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly.
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "QTile"
