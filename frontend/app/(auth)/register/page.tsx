"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRegister } from "@/lib/hooks/use-auth";

const schema = z.object({
  full_name: z.string().min(1, "Your name is required."),
  email: z.string().email("Enter a valid email address."),
  password: z
    .string()
    .min(8, "At least 8 characters.")
    .regex(/[a-z]/, "Include a lowercase letter.")
    .regex(/[A-Z]/, "Include an uppercase letter.")
    .regex(/\d/, "Include a number."),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const registerUser = useRegister();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Create your account</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Start analyzing your resume with AI in seconds.
      </p>

      <form onSubmit={handleSubmit((values) => registerUser.mutate(values))} className="mt-8 space-y-4">
        <div className="space-y-2">
          <Label htmlFor="full_name">Full name</Label>
          <Input id="full_name" placeholder="Ada Lovelace" autoComplete="name" {...register("full_name")} />
          {errors.full_name && <p className="text-xs text-rose-400">{errors.full_name.message}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@example.com" autoComplete="email" {...register("email")} />
          {errors.email && <p className="text-xs text-rose-400">{errors.email.message}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" placeholder="••••••••" autoComplete="new-password" {...register("password")} />
          {errors.password && <p className="text-xs text-rose-400">{errors.password.message}</p>}
        </div>

        <Button type="submit" variant="gradient" className="w-full" disabled={registerUser.isPending}>
          {registerUser.isPending && <Loader2 className="animate-spin" />}
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-primary hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
