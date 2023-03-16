### library
react-router5 \
react-hook-form \
react-query

### hook
useContext \
useEffect \
useMemo \
useState

### component
TypeScript Cheatsheets
```typescript
import React, { useState } from 'react';

interface IProps {
    title?: string;
    valid: boolean;
}
const Index: React.FC<IProps> = ({title,valid}) => {
    let [count, setCount] = useState(0);
    return(
        <div>
            <p>{title}</p>
            <p>{valid}</p>
            <p>{count}</p>
            <button onClick={() => setCount(count + 1)}>Click</button>
        </div>
    );
};
export default Index;

```