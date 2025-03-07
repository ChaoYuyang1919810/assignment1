"""
Song List 1.0 - by Yuyang Chao
Name: Yuyang Chao
Date started: 03-04-2025
GitHub URL:https://github.com/ChaoYuyang1919810/assignment1.git
Estimate: 8 h
Actual: 11 h
"""

# Constant for file name because teacher said to use them
SONGS_FILE = "songs.csv"
LEARNED_MARKER = "l"
UNLEARNED_MARKER = "u"


def main():
    """Main program logic"""
    print("Song List 1.0 - by Yuyang Chao")
    all_songs = load_songs_from_file()
    print(f"{len(all_songs)} songs loaded.\n")

    choice = ""
    while choice != "Q":
        show_menu()
        choice = input(">>> ").strip().upper()

        if choice == "D":
            show_song_list(all_songs)
        elif choice == "A":
            add_new_song(all_songs)
        elif choice == "C":
            mark_song_learned(all_songs)
        elif choice == "Q":
            save_songs_to_file(all_songs)
            print(f"\n{len(all_songs)} songs saved to {SONGS_FILE}")
            print("Make some music!")
        else:
            if choice:
                print("Invalid menu choice")
        print()


def show_menu():
    """Display menu options"""
    print("Menu:")
    print("D - Display songs")
    print("A - Add new song")
    print("C - Complete a song")
    print("Q - Quit")


def load_songs_from_file():
    """Read songs from CSV file"""
    song_list = []
    try:
        with open(SONGS_FILE, "r") as in_file:
            for line_number, line in enumerate(in_file, 1):
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue

                title = parts[0]
                artist = parts[1]
                try:
                    year = int(parts[2])
                    learned = parts[3] == LEARNED_MARKER
                    song_list.append([title, artist, year, learned])
                except ValueError:
                    print(f"Invalid year in line {line_number}")
        # Sort by year then title (case insensitive)
        song_list.sort(key=lambda s: (s[2], s[0].lower()))
    except FileNotFoundError:
        pass  # It's okay if file doesn't exist yet

    return song_list


def save_songs_to_file(songs):
    """Save songs to CSV file"""
    with open(SONGS_FILE, "w") as out_file:
        for song in songs:
            status = LEARNED_MARKER if song[3] else UNLEARNED_MARKER
            out_file.write(f"{song[0]},{song[1]},{song[2]},{status}\n")


def show_song_list(songs):
    """Display formatted list of songs"""
    if not songs:
        print("No songs to display")
        return

    learned = 0
    for song in songs:
        if song[3]:
            learned += 1

    # Calculate column widths for formatting
    max_title = max(len(s[0]) for s in songs) if songs else 0
    max_artist = max(len(s[1]) for s in songs) if songs else 0

    for i, song in enumerate(songs, 1):
        prefix = "* " if not song[3] else "  "
        print(f"{i}. {prefix}{song[0]:<{max_title}} - {song[1]:<{max_artist}} ({song[2]})")

    unlearned = len(songs) - learned
    print(f"\n{learned} songs learned, {unlearned} songs still to learn")


def add_new_song(song_list):
    """Add new song to list"""
    print("Enter details for new song")
    while True:
        title = input("Title: ").strip()
        if title:
            break
        print("Title can't be blank!")

    while True:
        artist = input("Artist: ").strip()
        if artist:
            break
        print("Artist can't be blank!")

    while True:
        year_str = input("Year: ").strip()
        if year_str.isdigit() and int(year_str) > 0:
            year = int(year_str)
            break
        print("Invalid year - must be positive number")

    song_list.append([title, artist, year, False])
    song_list.sort(key=lambda s: (s[2], s[0].lower()))
    print(f"\n{title} by {artist} ({year}) added")


def mark_song_learned(songs):
    """Mark song as learned"""
    unlearned = [s for s in songs if not s[3]]
    if not unlearned:
        print("No more songs to learn!")
        return

    while True:
        try:
            print("Enter song number to mark learned")
            num = int(input(">>> "))
            if 1 <= num <= len(songs):
                song = songs[num - 1]
                if song[3]:
                    print(f"You already know {song[0]}")
                else:
                    song[3] = True
                    print(f"Congratulations! Learned {song[0]}")
                break
            print("Invalid song number")
        except ValueError:
            print("Please enter a number")


if __name__ == "__main__":
    main()