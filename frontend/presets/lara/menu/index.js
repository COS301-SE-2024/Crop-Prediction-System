export default {
    root: {
        class: [
            // Sizing and Shape
            'min-w-[12rem]',
            'rounded-lg',
            // Spacing
            // 'py-2',
            // Colors
            'bg-surface-100 dark:bg-surface-800',
            'text-surface-700 dark:text-white/80',
            // 'border border-surface-200 dark:border-surface-700'
        ]
    },
    menu: {
        class: [
            // Spacings and Shape
            'list-none',
            'm-0',
            'p-0',
            'outline-none'
        ]
    },
    content: ({ context }) => ({
        class: [
            //Shape
            'rounded-lg',
            // Colors
            'text-surface-700 dark:text-white/80',
            {
                'bg-surface-200 text-surface-700 dark:bg-surface-300/10 dark:text-white': context.focused
            },
            // Transitions
            'transition-shadow',
            'duration-200',
            // States
            'hover:text-surface-700 dark:hover:text-white/80',
            'hover:bg-gray-300 dark:bg-surface-800 dark:hover:bg-surface-400/10',

        ]
    }),
    action: {
        class: [
            'relative',
            // Flexbox

            'flex',
            'items-center',

            // Spacing
            'py-3',
            'px-5',

            // Color
            'text-surface-700 dark:text-white/80',
            'bg-transparent',

            // Misc
            'no-underline',
            'overflow-hidden',
            'cursor-pointer',
            'select-none'
        ]
    },
    icon: {
        class: [
            // Spacing
            'mr-2',

            // Color
            'text-surface-600 dark:text-white/70'
        ]
    },
    label: {
        class: ['leading-none bg-surface-100 dark:bg-surface-800']
    },
    submenuheader: {
        class: [
            // Font
            'font-[500]',
            // Spacing
            'm-0',
            'pb-1 pt-3 px-5',
            // Shape
            'rounded-tl-none',
            'rounded-tr-none',
            // Colors
            'bg-surface-100 dark:bg-surface-800',
            'text-surface-700 dark:text-white'
        ]
    },
    transition: {
        enterFromClass: 'opacity-0 scale-y-[0.8]',
        enterActiveClass: 'transition-[transform,opacity] duration-[120ms] ease-[cubic-bezier(0,0,0.2,1)]',
        leaveActiveClass: 'transition-opacity duration-100 ease-linear',
        leaveToClass: 'opacity-0'
    }
};
