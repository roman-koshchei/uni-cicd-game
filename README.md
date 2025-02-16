# CI/CD Game

Game made with Python and Pygame for CI/CD classes in University.

Team:
- [Roman Koshchei](https://github.com/roman-koshchei)
- [Bohdan Starosivets](https://github.com/sinarhen)
- [Rostyslav Derkach](https://github.com/rostiksqx)


## Diagrams

We use Mermaid js to create and display diagrams. It's supported by GitHub as well. 

### Use Case Diagram

```mermaid
graph TD
  Player -->|Control| PacMan
  PacMan -->|Eats| Dots
  PacMan -->|Eats| PowerPellets
  PacMan -->|Avoids| Ghosts
  PacMan -->|Chases| FrightenedGhosts
  Ghosts -->|Chase| PacMan
  PacMan -->|Moves through| Maze
  Player -->|Starts| Game
  Player -->|Pauses| Game
  Player -->|Ends| Game
```
