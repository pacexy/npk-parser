# npk-parser
A parser for NPK(NeoplePack) file.

## Usage
```python
# import
from npk-parser import npk as NPK

# parse npk file
npk = NPK.parse('./npk/my-npk.NPK')
# do something
```

## Interface
```typescript
interface NPK {
    children: Image[]
}

interface Image {
    name: string
    size: number
    version: number
    children: Texture[]
}

interface Texture {
    type: string
    compress: string
    width?: number
    height?: number
    size?: number
    key_x?: number
    key_y?: number
    max_width?: number
    max_height?: number
    data?: byte[]
}
```