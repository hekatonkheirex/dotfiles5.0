import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

## Autostart programs ##
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

## Defaults ##
mod = "mod4"
#myTerm = "kitty"
myTerm = "alacritty"

keys = [
        ## The essentials ##
        Key(
            [mod], "Return", 
            lazy.spawn(myTerm), 
            desc="Launch terminal"
            ),
        #Key(
        #    [mod], "d", 
        #    lazy.spawncmd(),
        #    desc="Spawn a command using a prompt widget"
        #    ),
        Key(
            [mod, "shift"], "r", 
            lazy.restart(), 
            desc="Restart Qtile"
            ),
        Key(
            [mod, "shift"], "q", 
            lazy.shutdown(), 
            desc="Shutdown Qtile"
            ),
        Key(
            [mod], "w", 
            lazy.window.kill(), 
            desc="Kill focused window"
            ),
        Key(
            [mod], "Tab", 
            lazy.next_layout(), 
            desc="Toggle between layouts"
            ),

        ## Windows management ##
        Key(
            [mod], "h", 
            lazy.layout.left(), 
            desc="Move focus to left"
            ),
        Key(
            [mod], "l", 
            lazy.layout.right(), 
            desc="Move focus to right"
            ),
        Key(
            [mod], "j", 
            lazy.layout.down(), 
            desc="Move focus down"
            ),
        Key(
            [mod], "k", 
            lazy.layout.up(), 
            desc="Move focus up"
            ),
        Key(
            [mod], "space", 
            lazy.layout.next(),
            desc="Move window focus to other window"
            ),
        Key(
            [mod, "shift"], "h", 
            lazy.layout.shuffle_left(),
            desc="Move window to the left"
            ),
        Key(
            [mod, "shift"], "l", 
            lazy.layout.shuffle_right(),
            desc="Move window to the right"
            ),
        Key(
            [mod, "shift"], "j", 
            lazy.layout.shuffle_down(),
            desc="Move window down"
            ),
        Key(
            [mod, "shift"], "k", 
            lazy.layout.shuffle_up(), 
            desc="Move window up"
            ),
        Key(
            [mod, "control"], "h", 
            lazy.layout.grow_left(),
            desc="Grow window to the left"
            ),
        Key(
            [mod, "control"], "l", 
            lazy.layout.grow_right(),
            desc="Grow window to the right"
            ),
        Key(
            [mod, "control"], "j", 
            lazy.layout.grow_down(),
            desc="Grow window down"
            ),
        Key(
            [mod, "control"], "k", 
            lazy.layout.grow_up(), 
            desc="Grow window up"
            ),
        Key(
            [mod], "n", 
            lazy.layout.normalize(), 
            desc="Reset all window sizes"
            ),
        Key(
            [mod, "shift"], "Return", 
            lazy.layout.toggle_split(),                             # Split = all windows displayed; Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
            desc="Toggle between split and unsplit sides of stack"
            ),
        Key(
            [mod], "f",
            lazy.window.toggle_fullscreen(),
            desc="Toggle fullscreen"
            ),

        ## Custom keybinds ##
        Key(
            ["control", "mod1"], "l",
            lazy.spawn('betterlockscreen -l dimblur'),
            desc="Lock the screen"
            ),
        Key(
            [mod], "b",
            lazy.spawn('firefox'),
            desc="Launch Firefox"
            ),
        Key(
            [mod], "t",
            lazy.spawn('Thunar'),
            desc="Launch Thunar"
            ),
        Key(
            [mod], "d",
            lazy.spawn('rofi -show drun'),
            desc="Spawn rofi"
            ),

        ## Audio keybindings ##
        Key(
            [], "XF86AudioMute", 
            lazy.spawn("pactl set-sink-mute 0 toggle"),
            lazy.spawn("dunstify -i ~/.config/dunst/vmute.png 'Audio muted'"),
            desc="Mute audio"
            ),
        Key(
            [], "XF86AudioLowerVolume", 
            lazy.spawn("pactl set-sink-volume 0 -5%"),
            lazy.spawn("dunstify -i ~/.config/dunst/vdown.png 'Volume down'"),
            desc="Lower audio"
            ),
        Key(
            [], "XF86AudioRaiseVolume", 
            lazy.spawn("pactl set-sink-volume 0 +5%"),
            lazy.spawn("dunstify -i ~/.config/dunst/vup.png 'Volume up'"),
            desc="Raise audio"
            ),
        
        ## Screenshots ##
        Key(
            [], "Print",
            lazy.spawn("scrot 'screenshot_%Y%m%d_%H%M%S.png' -e 'mkdir -p ~/Pictures/Screenshots && mv $f ~/Pictures/Screenshots && xclip -selection clipboard -t image/png -i ~/Pictures/Screenshots/`ls     -1 -t ~/Pictures/Screenshots | head -1`'"),
            lazy.spawn("dunstify -i ~/.config/dunst/screenshot.png 'Screenshot captured'"),
            ),

        ## Touchpad ##
        Key(
            [], "XF86TouchpadToggle",
            lazy.spawn("/home/mura/.config/scripts/touchpad.sh toggle"),
            desc="Enable/disable touchpad"
            ),
]

## Workspaces/groups generation ##
#group_names = [("WWW", {'layout': 'monadtall'}),
#               ("DEV", {'layout': 'monadtall'}),
#               ("SYS", {'layout': 'monadtall'}),
#               ("DOC", {'layout': 'monadtall'}),
#               ("VBOX", {'layout': 'monadtall'}),
#               ("CHAT", {'layout': 'monadtall'}),
#               ("MUS", {'layout': 'monadtall'}),
#               ("VID", {'layout': 'monadtall'}),
#               ("GFX", {'layout': 'floating'})]

#groups = [Group(name, **kwargs) for name, kwargs in group_names]

#for i, (name, kwargs) in enumerate(group_names, 1):
#    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
#    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

__groups = {
        1: Group("󰈹", matches=[Match(wm_class=["firefox"])], layout='max'),
        2: Group("󰆍", matches=[Match(wm_class=["kitty", "Alacritty"])], layout='monadtall'),
        3: Group("󰙅", matches=[Match(wm_class=["Thunar"])], layout='max'),
        4: Group("󰈙", matches=[Match(wm_class=["Soffice"])], layout= 'max'),
        5: Group("󰒓", layout='floating'),
        6: Group("󰦗", matches=[Match(wm_class=["qBittorrent"])], layout='max'),
        7: Group("󰙯", matches=[Match(wm_class=["discord"])], layout='max'),
        8: Group("󱒃", matches=[Match(wm_class=["TeamViewer", "Anydesk"])], layout='floating'),
        9: Group("󰷝", matches=[Match(wm_class=["mpv"])], layout='floating'),
        0: Group("󰓇", matches=[Match(wm_class=["Spotify"])], layout='max'),
    }

groups = [__groups[i] for i in __groups]

def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(get_group_key(i.name)), 
            lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)
            ),

        # mod1+shift+letter of group = switch to & move focused window to group
        #Key([mod, "shift"], str(get_group_key(i.name)),
        #    lazy.window.togroup(i.name, switch_group=True),
        #    desc="Switch to & move focused window to group {}".format(i.name)
        #    ),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key(
            [mod, "shift"], str(get_group_key(i.name)), 
            lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)
            ),
        ])

## Layouts ##

layout_theme = {"border_width": 4,
                "margin": 15,
                "border_focus": "1a1a1a",
                "border_normal": "1a1a1a"
                }

layouts = [
        layout.Max(**layout_theme
            ),
        layout.MonadTall(
            border_focus = '1a1a1a',
            border_normal = '1a1a1a',
            border_width = 4,
            margin = 15,
            ratio = 0.52,
            ),
        layout.Floating(
            border_focus = '1a1a1a',
            border_normal = '1a1a1a',
            border_width = 4,
            fullscreen_border_width = 0,
            ),
        #layout.Columns(**layout_theme),
        #layout.Stack(num_stacks=2),
        #layout.Bsp(**layout_theme),
        #layout.Matrix(**layout_theme),
        layout.MonadWide(**layout_theme),
        #layout.RatioTile(**layout_theme),
        layout.Tile(**layout_theme),
        #layout.TreeTab(**layout_theme),
        #layout.VerticalTile(**layout_theme),
        #layout.Zoomy(**layout_theme)
    ]

## Colors definitions ##
colors = [["#1a1a1a", "#1a1a1a"], # 0 Background 0
          ["#303030", "#303030"], # 1 Background 1
          ["#f6f6ef", "#f6f6ef"], # 2 Foreground 0
          ["#c4c5b5", "#c4c5b5"], # 3 Foreground 1
          ["#f4005f", "#f4005f"], # 4 Red
          ["#98e924", "#98e924"], # 5 Green
          ["#e6db74", "#e6db74"], # 6 Yellow
          ["#58d1eb", "#58d1eb"], # 7 Blue
          ["#fd5ff0", "#fd5ff0"], # 8 Magenta
          ["#a1efe4", "#a1efe4"], # 9 Cyan
          ["#fa8419", "#fa8419"], # 10 Orange
          ["#9d65ff", "#9d65ff"], # 11 Violet
          ]


prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

## Widgets definitions ##
widget_defaults = dict(
    #font = 'SF Pro Display',
    font = 'Ubuntu Medium',
    fontsize = 14,
    padding = 4,
    background = '#1a1a1a',
    foreground = '#f6f6ef',
)

extension_defaults = widget_defaults.copy()

screens = [
        Screen(
            top=bar.Bar(
                [
                    widget.GroupBox(
                        active = colors[2],
                        block_highlight_text_color = colors[11],
                        borderwidth = 2,
                        disable_drag = True,
                        fontsize = 18,
                        hide_unused = False,
                        highlight_color = '00000000',
                        highlight_method = 'line',
                        inactive = colors[1],
                        padding = 2,
                        rounded = True,
                        spacing = 1,
                        this_current_screen_border = colors[8],
                        urgent_alert_method = 'line',
                        urgent_border = colors[4],
                        urgent_text = colors[4],
                        ),
                    widget.CurrentLayout(
                        padding = 4,
                        foreground = colors[5],
                        ),
                    widget.Mpris2(
                        name = 'spotify',
                        objname = "org.mpris.MediaPlayer2.spotify",
                        display_metadata = ['xesam:title', 'xesam:artist'],
                        scroll_chars = None,
                        stop_pause_text = '',
                        padding = 4,
                        foreground = colors[9],
                        ),
                    widget.Mpd2(
                        idle_format = '{idle_message}',
                        idle_message = '',
                        max_chars = 20,
                        padding = 4,
                        status_format = '{play_status} {title} - {artist}',
                        foreground = colors[7],
                        ),
                    #widget.Prompt(
                    #    background = colors[0],
                    #    bell_style = 'visual',
                    #    cursor = True,
                    #    cursor_color = colors[4],
                    #    cursorblink = 1,
                    #    foreground = colors[4],
                    #    max_history = 5,
                    #    padding = 1,
                    #    prompt = '{prompt}: ',
                    #    record_history = True,
                    #    visual_bell_color = colors[4],
                    #    visual_bell_time = 0.3,
                    #    ),
                    #widget.TextBox(
                    #    text = '󰘔',
                    #    padding = 1,
                    #    fontsize = 16,
                    #    ),
                    #widget.WindowName(
                    #    max_chars = 60,
                    #    padding = 1,
                    #    ),
                    widget.Spacer(
                            ),
                    widget.CheckUpdates(
                            update_interval = 1800,
                            distro = "Arch_checkupdates",
                            display_format = "󰏗 {updates}",
                            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e yay -Syu')},
                            no_updates_string = '0',
                            padding = 4,
                            ),
                    #widget.Wlan(
                    #        format = '󰖩 {essid}',
                    #        interface = 'wlp1s0',
                    #        padding = 4,
                    #        foreground = colors[11],
                    #        ),
                    widget.TextBox(
                            text = '󰌓',
                            padding = 2,
                            foreground = colors[8],
                            ),
                    widget.KeyboardLayout(
                            configured_keyboards = ['us', 'es'],
                            option = 'compose:menu,grp_led:scroll',
                            padding = 2,
                            update_interval = 1,
                            foreground = colors[8],
                            ),
                    #widget.Backlight(
                    #        backlight_name = 'amdgpu_bl0',
                    #        brightness_file = 'brightness',
                    #        change_command = 'light -S {0}',
                    #        format = '󱍖{percent:5.0%}',
                    #        max_brightness_file = 'max_brightness',
                    #        padding = 4,
                    #        step = 5,
                    #        ),
                    widget.TextBox(
                            text = '󰕾',
                            padding = 2,
                            foreground = colors[8],
                            ),
                    widget.PulseVolume(
                            padding = 2,
                            foreground = colors[8],
                            ),
                    widget.CPU(
                            format = '󰻠 {load_percent}%',
                            foreground = colors[10],
                            ),
                    widget.Memory(
                            format = '󰍛 {MemUsed: .0f} M',
                            measure_mem = 'M',
                            update_interval = 1.0,
                            foreground = colors[10],
                            ),
                    widget.TextBox(
                            text = '󰔏',
                            padding = 2,
                            foreground = colors[10],
                            ),
                    widget.ThermalSensor(
                            foreground = colors[10],
                            ),
                    #widget.Battery(
                    #        charge_char = '󰂄',
                    #        discharge_char = '󰂃',
                    #        empty_char = '󱃍',
                    #        full_char = '󰁹',
                    #        format = '{char} {percent:2.0%}',
                    #        padding = 2,
                    #        unknown_char = '󰂑',
                    #        update_interval = 60,
                    #        ),
                    widget.Clock(
                            format='󰃰 %a, %b %d | %H:%M |',
                            padding = 2,
                            foreground = colors[6],
                            ),
                    widget.OpenWeather(
                            app_key = '29c7c3f06ff45f58f6a2e409c2fb2d22',
                            cityid = '3439389',
                            format = '{weather_details} {main_temp}°{units_temperature}',
                            metric = True,
                            #mouse_callbacks = {'Button1': url},
                            padding = 2,
                            update_interval = 600,
                            url = 'https://openweathermap.org/city/3439389',
                            foreground = colors[6],
                            ),
                    widget.Systray(
                            padding = 5,
                            ),
                    widget.QuickExit(
                            countdown_format = '[ {} ]',
                            foreground = colors[4],
                            default_text = ' [󰁕] ',
                            padding = 2,
                            ),
                ],
            30,
        ),
    ),
]

## Drag floating layouts ##
mouse = [
        Drag(
            [mod], "Button1", 
            lazy.window.set_position_floating(),
            start=lazy.window.get_position()
            ),
        Drag(
            [mod], "Button3", 
            lazy.window.set_size_floating(),
            start=lazy.window.get_size()
            ),
        Click(
            [mod], "Button2", 
            lazy.window.bring_to_front()
            )
]

## General configurations ##
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
        border_focus = '1a1a1a',
        border_normal = '1a1a1a',
        border_width = 2,
        fullscreen_border_width = 0,
        float_rules=[
            # Run the utility of `xprop` to see the wm class and name of an X client.
            *layout.Floating.default_float_rules,
            Match(wm_class='confirmreset'),  # gitk
            Match(wm_class='makebranch'),  # gitk
            Match(wm_class='maketag'),  # gitk
            Match(wm_class='ssh-askpass'),  # ssh-askpass
            Match(title='branchdialog'),  # gitk
            Match(title='pinentry'),  # GPG key password entry
            Match(wm_class='Galculator'),
        ]
    )
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
