import React from "react"
import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast.jsx"

export function Toaster() {
  const [toasts, setToasts] = React.useState([])

  React.useEffect(() => {
    window.addToast = ({ title, description, variant = "default" }) => {
      const id = Date.now()
      setToasts(prev => [...prev, { id, title, description, variant }])
      setTimeout(() => {
        setToasts(prev => prev.filter(toast => toast.id !== id))
      }, 5000)
    }
  }, [])

  return (
    <ToastProvider>
      {toasts.map(({ id, title, description, variant }) => (
        <Toast key={id} variant={variant}>
          <div className="grid gap-1">
            {title && <ToastTitle>{title}</ToastTitle>}
            {description && <ToastDescription>{description}</ToastDescription>}
          </div>
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProvider>
  )
}

export const toast = ({ title, description, variant = "default" }) => {
  if (window.addToast) {
    window.addToast({ title, description, variant })
  }
}